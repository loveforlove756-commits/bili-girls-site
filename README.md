# bili娘站

展示 73 位 bili娘（站娘选举）角色信息的 Streamlit 网站，支持按编号/名称检索、查看详情弹窗。

## 在线访问

由 Streamlit Community Cloud 托管。

## 本地运行

```bash
pip install -r requirements.txt
streamlit run wz.py
```

## 说明

- 角色数据内联在 `wz.py` 中，无需额外 JSON 数据文件
- 图片以 base64 文本（`.b64`）形式随仓库分发，运行时自动解码，便于在云端环境显示
- 作者：[忆人摘星](https://space.bilibili.com/3546929877224366)
