# draw.io Mermaid URL 编码分析报告

## 问题概述

drawio-mcp 插件生成的 URL 在 draw.io 中打开时报错，URL 中的 base64 数据被双重编码。

## 当前代码（错误）

```typescript
// Mermaid 格式
const base64 = Buffer.from(content, "utf-8").toString("base64");
const encoded = encodeURIComponent(base64);
return `https://app.diagrams.net/#R${encoded}`;
```

## 根本原因分析

### 1. 使用了错误的 URL 参数

**`#R` 参数的用途**：
- 用于传递 **draw.io XML 格式**的原始图数据
- 数据需要经过：XML → 压缩（deflate）→ Base64 → URI 编码
- 官方文档明确说明："This must be URI encoded"

**正确的 Mermaid 参数应该是 `create`**：
- 用于创建新文件
- 支持 JSON 对象：`{type: 'mermaid', data: 'mermaid_code'}`
- JSON 对象需要 URL 编码

### 2. 编码错误

当前代码的问题：
```typescript
// 错误 1: #R 不适用于 Mermaid 代码
// 错误 2: 对 Mermaid 代码进行 base64 编码是错误的
// 错误 3: 对 base64 进行 encodeURIComponent 导致双重编码
// （base64 中的 % 变成 %25，+ 变成 %2B，/ 变成 %2F，= 变成 %3D）
```

## 正确的解决方案

### 方案 1：使用 `create` 参数（推荐）

```typescript
function createDrawioUrlForMermaid(mermaidCode: string): string {
  // 构造 JSON 对象
  const jsonData = JSON.stringify({
    type: 'mermaid',
    data: mermaidCode
  });

  // 对 JSON 进行 URL 编码
  const encoded = encodeURIComponent(jsonData);

  // 返回完整的 URL
  return `https://app.diagrams.net/?create=${encoded}`;
}

// 示例
const mermaidCode = `graph TD;
  A-->B;
  A-->C;
  B-->D;
  C-->D;`;

const url = createDrawioUrlForMermaid(mermaidCode);
// 结果: https://app.diagrams.net/?create=%7B%22type%22%3A%22mermaid%22%2C%22data%22%3A%22graph%20TD%3B%5C%5Cn%20%20A--%3EB%3B%5C%5Cn%20%20A--%3EC%3B%5C%5Cn%20%20B--%3ED%3B%5C%5Cn%20%20C--%3ED%3B%22%7D
```

### 方案 2：使用 `#R` 参数（仅适用于 draw.io XML）

如果一定要用 `#R`，需要先转换为 draw.io XML：

```typescript
// 注意：这不是用于 Mermaid，而是用于 draw.io XML
import zlib from 'zlib';

function createDrawioUrlForXml(xmlData: string): string {
  // 1. 压缩数据（使用 deflate）
  const compressed = zlib.deflateSync(xmlData);

  // 2. Base64 编码
  const base64 = compressed.toString('base64');

  // 3. URI 编码（这是必需的！）
  const encoded = encodeURIComponent(base64);

  return `https://app.diagrams.net/#R${encoded}`;
}
```

## 官方文档参考

### draw.io Location Hash 属性文档
来源：https://www.drawio.com/doc/faq/supported-location-hash-properties

```
R{data}: Passes the raw diagram data (example)
This must be URI encoded.

示例: https://app.diagrams.net/?lightbox=1#R7ZjLcpswFIafhmU...
```

### draw.io URL 参数文档
来源：https://www.drawio.com/doc/faq/supported-url-parameters

```
create=url/name/json: Creates a new file from a template URL.
If the value starts with a {, it is treated as a JSON object.
Currently supported objects are {type: 'type', data: 'data'}
where type can be one of xml, mermaid, csv or message

示例: https://app.diagrams.net/?create=%7B%22type%22%3A%22mermaid%22%2C%22data%22%3A%22graph%20TD%3B%5C%5CnA--%3EB%3B%5C%5CnA--%3EC%3B%5C%5CnB--%3ED%3B%5C%5CnC--%3ED%3B%22%7D
```

## 代码修复建议

### 修改前（错误）

```typescript
// Mermaid 格式
const base64 = Buffer.from(content, "utf-8").toString("base64");
const encoded = encodeURIComponent(base64);
return `https://app.diagrams.net/#R${encoded}`;
```

### 修改后（正确）

```typescript
// Mermaid 格式 - 使用 create 参数
const jsonData = JSON.stringify({
  type: 'mermaid',
  data: content  // 直接使用原始 Mermaid 代码
});
const encoded = encodeURIComponent(jsonData);
return `https://app.diagrams.net/?create=${encoded}`;
```

## 测试验证

### 正确的 URL 示例

```bash
# Mermaid 示例（使用 create）
https://app.diagrams.net/?create=%7B%22type%22%3A%22mermaid%22%2C%22data%22%3A%22graph%20TD%3B%5C%5CnA--%3EB%3B%5C%5CnA--%3EC%3B%5C%5CnB--%3ED%3B%5C%5CnC--%3ED%3B%22%7D

# 解码后的数据：
# {"type":"mermaid","data":"graph TD;\nA-->B;\nA-->C;\nB-->D;\nC-->D;"}
```

### 错误的 URL 示例（当前代码生成的）

```bash
# 如果使用当前的错误代码：
# 1. Mermaid 代码: "graph TD; A-->B;"
# 2. Base64: "Z3JhcGggVEQ7IEEtLT5COw=="
# 3. URI 编码: "Z3JhcGggVEQ7IEEtLT5COw%3D%3D"
# 4. 最终 URL: https://app.diagrams.net/#RZ3JhcGggVEQ7IEEtLT5COw%3D%3D

# 问题：
# - draw.io 期望 #R 后面是压缩的 XML 数据（base64 编码）
# - 但这里得到的是未压缩的 Mermaid 代码的 base64
# - draw.io 无法解析，会报错
```

## 总结

1. **使用正确的参数**：Mermaid 应该用 `create`，而不是 `#R`
2. **不要对 Mermaid 进行 base64 编码**：直接传递原始代码
3. **正确编码 JSON**：使用 `JSON.stringify` + `encodeURIComponent`
4. **如果要用 `#R`**：必须先转换为 draw.io XML 并压缩

## 推荐修复代码

```typescript
/**
 * 为 Mermaid 代码创建 draw.io URL
 * @param mermaidCode - Mermaid 图表代码
 * @returns draw.io URL
 */
export function createDrawioMermaidUrl(mermaidCode: string): string {
  const jsonData = JSON.stringify({
    type: 'mermaid',
    data: mermaidCode
  });
  const encoded = encodeURIComponent(jsonData);
  return `https://app.diagrams.net/?create=${encoded}`;
}
```

---

**分析日期**: 2026-03-07
**分析者**: Subagent (glm-5 model)
**任务**: 分析 draw.io Mermaid URL 编码问题并给出修复方案
