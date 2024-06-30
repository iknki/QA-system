import numpy as np
import pandas as pd
import os
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
import joblib


# 定义自编码器模型
class Autoencoder(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, hidden_dim), nn.ReLU())
        self.decoder = nn.Sequential(nn.Linear(hidden_dim, input_dim), nn.Sigmoid())

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

class RecommendModelApi:

    def __init__(self, model_base_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.device = torch.device("cpu")
        self.model_base_path = model_base_path
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        self.bert_model = BertModel.from_pretrained('bert-base-chinese').to(self.device)

    # 训练模型
    def train_model(self, questions, model_name):
        # 提取问题的BERT表示
        question_embeddings = []
        for question in questions:
            inputs = self.tokenizer(
                question,
                return_tensors="pt",
                max_length=128,
                truncation=True,
                padding="max_length",
            )
            with torch.no_grad():
                outputs = self.bert_model(**inputs.to(self.device))
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
            question_embeddings.append(embeddings)

        question_embeddings = np.array(question_embeddings)  # 将列表转换为NumPy数组

        # 训练自编码器
        input_dim = question_embeddings.shape[1]  # 输入维度等于问题表示的维度
        hidden_dim = 64  # 自编码器隐藏层维度
        autoencoder = Autoencoder(input_dim, hidden_dim).to(self.device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(autoencoder.parameters(), lr=0.001)
        num_epochs = 10
        batch_size = 32
        for epoch in range(num_epochs):
            total_loss = 0.0
            for i in range(0, len(question_embeddings), batch_size):
                batch_data = (
                    torch.tensor(question_embeddings[i : i + batch_size]).float().cuda()
                )
                optimizer.zero_grad()
                outputs = autoencoder(batch_data)
                loss = criterion(outputs, batch_data)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            print(
                f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss / (len(question_embeddings) / batch_size)}"
            )

            # 使用自编码器进行聚类
            encoded_data = (
                autoencoder.encoder(torch.tensor(question_embeddings).float().cuda())
                .detach()
                .cpu()
                .numpy()
            )
            kmeans = KMeans(n_clusters=12, random_state=0).fit(encoded_data)
            clusters = kmeans.labels_

            # 将聚类结果添加到数据集中
            df = pd.DataFrame(questions, columns=["title"])
            df["cluster"] = clusters

            # 保存训练好的数据
            path = self.model_base_path + model_name
            # 创建模型文件夹
            if not os.path.exists(path):
                os.makedirs(path)
            path = path + "/" + model_name
            # 将question_embeddings保存到本地
            np.save(path + ".npy", question_embeddings)

            # 保存带有聚类标签的数据集
            df.to_csv(path + ".csv", index=False)

            # 保存自编码器模型
            torch.save(autoencoder.state_dict(), path + ".pth")

            # 保存K均值聚类模型
            joblib.dump(kmeans, path + ".pkl")

    # 加载模型
    def load_model(self, model_name):
        path = self.model_base_path + model_name + "/" + model_name
        self.question_embeddings = np.load(path + ".npy")
        self.autoencoder = Autoencoder(self.question_embeddings.shape[1], 64).to(self.device)
        self.autoencoder.load_state_dict(torch.load(path + ".pth"))
        self.autoencoder.eval()
        self.kmeans = joblib.load(path + ".pkl")
        self.df = pd.read_csv(path + ".csv")

    # 推荐问题
    async def recommend_similar_questions(self, question, top_n=10, model_name=None):
        if model_name:
            self.load_model(model_name)

        # 对输入问题进行编码
        inputs = self.tokenizer(
            question,
            return_tensors="pt",
            max_length=128,
            truncation=True,
            padding="max_length",
        )
        with torch.no_grad():
            outputs = self.bert_model(**inputs.to(self.device))
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

        # 获取输入问题所属的聚类标签
        encoded_data = (
            self.autoencoder.encoder(torch.tensor(embeddings).float().to(self.device))
            .detach()
            .cpu()
            .numpy()
        )
        # 将encoded_input转换为二维数组,然后预测类别
        cluster_label = self.kmeans.predict(encoded_data.reshape(1, -1))[0]
        # 获取该聚类中的所有问题
        cluster_data = self.df[self.df["cluster"] == cluster_label]
        similarities = []

        # 计算输入问题与聚类中所有问题的相似度
        for i, row in cluster_data.iterrows():
            other_embedding = self.question_embeddings[i]
            similarity = np.dot(embeddings, other_embedding) / (
                np.linalg.norm(embeddings) * np.linalg.norm(other_embedding)
            )
            similarities.append(similarity)
        indices = np.argsort(similarities)[::-1][1:top_n+1]
        return cluster_data.iloc[indices]['title'].tolist()
