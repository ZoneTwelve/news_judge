#!/bin/zsh

# split result
input="### 輸出結果
1. 犯罪人與公司: 康和期
2. 刑責: 裁罰
3. 刑責進度: 5項缺失，包括未就客戶財力與信用狀況綜合評估風險承擔程度、核定交易額度，客戶未提供財力證明申請即放寬交易額度，客戶對帳單寄送至業務員電子郵件信箱，內部人員帳戶未以適當方式與其他委託人區分。此外，出現非內部人員電子下單IP位址與公司內部網路IP位址相同。
4. 摘要: 金管會對康和期裁罰60萬元，並對葉姓、王姓及阮姓3名業務員停職1個月，原因是康和期存在多項缺失，包括未評估客戶風險承擔程度、核定交易額度，客戶未提供財力證明即放寬交易額度，客戶對帳單寄送至業務員電子郵件信箱，內部人員帳戶未與其他委託人區分。此外，康和期還出現非內部人員使用公司內部網路IP位址下單的情況。"

# Extract "犯罪人與公司"
criminal_company=$(echo "$input" | sed -n 's/^1\. 犯罪人與公司: \(.*\)$/\1/p')

# Extract "刑責"
criminal_penalty=$(echo "$input" | sed -n 's/^2\. 刑責: \(.*\)$/\1/p')

# Extract "刑責進度"
criminal_progress=$(echo "$input" | sed -n 's/^3\. 刑責進度: \(.*\)$/\1/p')

# Extract "摘要"
summary=$(echo "$input" | sed -n 's/^4\. 摘要: \(.*\)$/\1/p')

echo "主體: $criminal_company"
echo "刑責: $criminal_penalty"
echo "刑責進度: $criminal_progress"
echo "摘要: $summary"

# split result end

# split data
# data="犯罪人與公司: 元富期, 康和期, 群益期, 凱基期, 永豐期, 元大期, 日盛期, 群益證"

# # content=$(echo "$data" | grep -o '(?<=犯罪人與公司: ).*')
# content=$(echo "$data" | sed 's/犯罪人與公司: //')
# delimiter=","

# # Split the string into an array using awk
# array=($(awk -F"$delimiter" '{for (i=1; i<=NF; i++) print $i}' <<< "$content"))

# # Print the array elements
# for element in "${array[@]}"; do
#   echo "$element"
# done
# split data end
