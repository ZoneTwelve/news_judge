# Prompt Engineering Guide

Learn how to create and optimize prompts for the News Inferencer.

## Table of Contents

- [Overview](#overview)
- [Prompt Structure](#prompt-structure)
- [Creating Prompts](#creating-prompts)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Optimization Tips](#optimization-tips)

## Overview

The News Inferencer uses a two-role prompt system compatible with OpenAI's Chat Completion API:

1. **System Prompt**: Defines the AI's role, expertise, and behavior
2. **User Prompt**: Provides the specific task and input data

## Prompt Structure

### System vs User Prompts

**System Prompt** (`*_system.txt`):
- Establishes AI's role and expertise
- Sets output format requirements
- Defines constraints and behavior

**User Prompt** (`*_user.txt`):
- Contains actual input data
- Specifies the task
- Includes variable placeholders

### Variable Placeholders

Use `$variable_name` syntax for dynamic content:

```text
分析以下新聞內容：
$news_content

請根據這些刑責關鍵字：
$crime_keywords
```

## Creating Prompts

### Step 1: Design Your Analysis

Determine:
1. What information to extract
2. Output format (structured/unstructured)
3. Required accuracy level
4. Language and tone

### Step 2: Write System Prompt

Create `prompts/my_system.txt`:

```text
你是一位專業的法律分析助手，專門分析新聞文章中的法律責任。

你的任務是：
1. 仔細閱讀新聞內容
2. 識別文章中提到的所有主體（人物、組織）
3. 判斷每個主體是否涉及法律責任

輸出格式：
請以逗號分隔的列表形式輸出所有識別到的主體名稱。

例如：張三, 李四, ABC公司

注意事項：
- 只輸出主體名稱，不要額外說明
- 確保名稱準確，保持原文中的稱呼
- 如果沒有識別到任何主體，輸出「無」
```

### Step 3: Write User Prompt

Create `prompts/my_user.txt`:

```text
新聞內容：
$news_content

刑責關鍵字參考：
$crime_keywords

判斷關鍵字參考：
$judge_keywords

請分析上述新聞內容，識別所有相關主體。
```

### Step 4: Create Configuration

Create `prompts/my_config.json`:

```json
{
  "name": "My Custom Analyzer",
  "files": {
    "system": "my_system.txt",
    "user": "my_user.txt"
  },
  "inputs": [
    "news_content",
    "crime_keywords",
    "judge_keywords"
  ]
}
```

### Step 5: Test Your Prompt

```bash
./prompt.py --config prompts/my_config.json \
            --news-content samples/case1/news_content.txt \
            --crime-keywords samples/crime_keywords.txt \
            --judge-keywords samples/judge_keywords.txt
```

## Best Practices

### 1. Clear Role Definition

**Good**:
```text
你是一位資深的刑事法律專家，擁有20年的案件分析經驗。
你的專長是從新聞報導中識別潛在的刑事責任。
```

**Bad**:
```text
你是AI助手。
```

### 2. Specific Output Format

**Good**:
```text
### 輸出格式

主體: [主體名稱]
是否有嫌疑: [是/否]
刑責: [刑責關鍵字，逗號分割]
刑責進度: [進度關鍵字，逗號分割]
事件摘要: [50字以內摘要]
```

**Bad**:
```text
請分析並輸出結果。
```

### 3. Provide Examples

**Good**:
```text
### 範例

輸入：張三涉嫌詐欺，已被檢察官起訴。
輸出：
主體: 張三
是否有嫌疑: 是
刑責: 詐欺
刑責進度: 起訴
事件摘要: 張三因涉嫌詐欺罪遭檢察官提起公訴。
```

**Bad**:
```text
請按照格式輸出。
```

### 4. Set Constraints

**Good**:
```text
注意事項：
- 僅基於新聞內容進行分析，不要推測
- 如果資訊不足，請標註「資訊不足」
- 保持客觀中立，避免主觀判斷
- 確保所有關鍵字都來自提供的列表
```

**Bad**:
```text
請分析。
```

### 5. Handle Edge Cases

```text
特殊情況處理：
- 如果沒有提到任何主體，輸出「無」
- 如果主體眾多（超過10個），僅列出最相關的10個
- 如果新聞內容為空，輸出「無法分析」
- 如果遇到法律專有名詞，保持原文
```

## Examples

### Example 1: Subject Extractor

**System Prompt**:
```text
你是專業的實體識別專家，專門從中文新聞中提取人名和組織名稱。

任務：識別新聞中所有相關的主體（包括人物和組織）

輸出格式：以逗號分隔的列表
範例：王小明, 李大華, XYZ科技公司

規則：
1. 只輸出主體名稱，不添加其他文字
2. 保持原文中的稱呼方式
3. 去除重複項
4. 按照出現順序排列
```

**User Prompt**:
```text
請從以下新聞中提取所有主體：

$news_content

參考關鍵字（用於判斷相關性）：
$crime_keywords
```

### Example 2: Legal Liability Inferencer

**System Prompt**:
```text
你是資深刑事律師，專長是分析新聞報導中的法律責任。

對於指定的主體，你需要：
1. 判斷是否涉及刑事責任
2. 識別具體的罪名
3. 確定案件進度
4. 提供簡要摘要

### 輸出格式

主體: [目標主體名稱]
是否有嫌疑: [是/否]
刑責: [相關罪名，用逗號分隔]
刑責進度: [起訴/羈押/判決等，用逗號分隔]
事件摘要: [50字內的簡要說明]

### 判斷標準

- 只有明確提到的罪名才列出
- 進度詞彙必須來自提供的關鍵字列表
- 如果資訊不明確，標註「資訊不足」
```

**User Prompt**:
```text
新聞內容：
$news_content

目標主體：$target

刑責關鍵字：
$crime_keywords

刑責進度關鍵字：
$judge_keywords

請分析目標主體的法律責任狀況。
```

### Example 3: Structured JSON Output

**System Prompt**:
```text
你是法律分析AI，輸出結構化的JSON格式結果。

輸出格式（嚴格JSON）：
{
  "subject": "主體名稱",
  "has_liability": true/false,
  "crimes": ["罪名1", "罪名2"],
  "legal_status": ["狀態1", "狀態2"],
  "summary": "事件摘要",
  "confidence": "high/medium/low"
}

規則：
- 必須是有效的JSON
- 所有字段都必須存在
- crimes和legal_status是數組，可為空[]
- 不要添加任何JSON之外的文字
```

**User Prompt**:
```text
{
  "news_content": "$news_content",
  "target": "$target",
  "crime_keywords": "$crime_keywords",
  "judge_keywords": "$judge_keywords"
}

請分析並以JSON格式返回結果。
```

## Optimization Tips

### 1. Temperature Settings

```python
# For consistent, deterministic legal analysis
temperature = 0.0

# For exploratory analysis with variations
temperature = 0.3

# Not recommended for legal work
temperature = 1.0  # Too random
```

### 2. Token Management

**Reduce Output Tokens**:
```text
摘要限制：最多50字
關鍵字：最多列出5個
```

**Efficient Input**:
```text
# Instead of full article
只需分析以下摘要：[提供摘要]

# Or focus on relevant sections
只需分析與法律相關的段落
```

### 3. Iterative Improvement

1. **Test with samples**: Run on known cases
2. **Analyze failures**: Where did it go wrong?
3. **Refine rules**: Add specific constraints
4. **Re-test**: Verify improvements
5. **Version control**: Keep track of changes

### 4. A/B Testing

Compare different prompt strategies:

```bash
# Test Version A
./prompt.py --config prompts/inferencer_v7.json ...

# Test Version B
./prompt.py --config prompts/inferencer_v8.json ...

# Compare results
diff output_v7.txt output_v8.txt
```

### 5. Prompt Chaining

For complex analysis, chain multiple prompts:

```
Step 1: Extract subjects
   ↓
Step 2: For each subject, analyze liability
   ↓
Step 3: Aggregate results
   ↓
Step 4: Generate summary report
```

## Common Pitfalls

### 1. Vague Instructions

**Problem**:
```text
請分析新聞。
```

**Solution**:
```text
請分析新聞中提到的所有主體，並判斷每個主體是否涉及以下罪名：[具體列出罪名]
```

### 2. Inconsistent Output

**Problem**: Output format varies between runs

**Solution**: Provide strict format with examples
```text
### 嚴格格式要求

必須按照以下格式輸出，不得有任何偏差：

主體: [名稱]
嫌疑: [是/否]

錯誤示例（不要這樣）：
主體是張三，他有嫌疑

正確示例（這樣才對）：
主體: 張三
嫌疑: 是
```

### 3. Over-Inference

**Problem**: AI makes assumptions beyond the text

**Solution**:
```text
重要限制：
- 僅基於新聞明確提到的內容
- 不要推測未提及的資訊
- 如果資訊不足，明確標註「不明確」
- 不要添加外部知識
```

### 4. Language Mixing

**Problem**: Output mixes Chinese and English

**Solution**:
```text
語言要求：
- 所有輸出必須使用繁體中文
- 專有名詞保持原文（如公司名）
- 不要使用英文進行說明
```

## Validation

### Test Checklist

- [ ] Format is consistent across multiple runs
- [ ] All required fields are present
- [ ] No hallucinated information
- [ ] Keywords match provided lists
- [ ] Edge cases handled properly
- [ ] Output is parseable (if structured)
- [ ] Reasonable response time
- [ ] Acceptable token usage

### Quality Metrics

Track these metrics for prompt performance:

- **Accuracy**: Correct vs total analyses
- **Consistency**: Same input → same output
- **Completeness**: All fields populated
- **Parsability**: Can be programmatically parsed
- **Cost**: Average tokens per analysis

## Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)

---

**Related Documentation**:
- [Configuration Guide](CONFIGURATION.md)
- [API Reference](API_REFERENCE.md)
- [Architecture Guide](ARCHITECTURE.md)
