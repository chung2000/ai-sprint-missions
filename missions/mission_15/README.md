# 🐳 Docker-based ML Collaboration Pipeline (Mission 15)

이 프로젝트는 두 명의 연구자가 협업하는 시나리오를 가정하여, **Docker Compose**를 활용한 머신러닝 파이프라인 자동화 및 데이터 공유 워크플로우를 구축한 결과물입니다.

## 📌 Project Overview
- **목표:** 독립된 컨테이너 간의 효율적인 데이터 공유 및 ML 파이프라인(학습-추론) 구축
- **핵심 기술:** Docker, Docker Compose, Python, Scikit-learn, Jupyter Notebook
- **데이터셋:** Student Performance Prediction Dataset (Regression)

## 🏗️ Architecture
이 프로젝트는 **Shared Volume Strategy**를 사용하여 호스트와 두 개의 컨테이너 간 데이터를 공유합니다.

```mermaid
graph TD
    subgraph Host["Host Computer (Local)"]
        DataDir[/"./data (Volume)"/]
    end

    subgraph Container1["Researcher 1 (Training)"]
        PyScript["train.py"]
    end

    subgraph Container2["Researcher 2 (Inference)"]
        Jupyter["Jupyter Notebook"]
    end

    PyScript -- "1. Save Model & Preprocessing" --> DataDir
    DataDir -- "2. Load Model & Test Data" --> Jupyter
    Jupyter -- "3. Save Result" --> DataDir
    
    style DataDir fill:#f9f,stroke:#333,stroke-width:2px