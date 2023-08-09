#!/bin/zsh
source submit.sh
source get_host.sh

# keys=('www.ettoday.net' 'www.chinatimes.com' 'udn.com' 'news.ltn.com.tw' 'finance.ettoday.net' 'ctee.com.tw')
# values=('//*[@id="society"]/div[4]/div[2]/div[9]/div/div/div[1]/div[1]/article/div' '//*[@id="page-top"]/div/div[2]/div/div/article/div/div[1]/div[2]/div[2]/div[2]' '/html/body/main/div/section[2]/section/article/div/section[1]' '//*[@id="ltnRWD"]/div[10]/section/div[4]/div[2]' '//*[@id="finance"]/div[3]/div[2]/div[7]/div/div[1]/div[1]/div[2]/div[4]' '//*[@id="post--24779"]/div[3]')
# declare -A xpaths
# for ((i=0; i<${#keys[@]}; i++)); do
#     xpaths[${keys[i]}]=${values[i]}
# done
# NEWS_CONTENT=$1
# get news_content from input pipeline
NEWS_URL=$1
NEWS_CONTENT=$(cat)
# echo "NEWS_CONTENT: $NEWS_CONTENT"
# exit

# check output.csv exist or not, if not create it with default header
if [ ! -f outputs/output.csv ]; then
    echo "新聞連結,犯罪人與公司,刑責,刑責進度,摘要" >> outputs/output-A.csv
fi
declare -A xpaths=(
    ['www.ettoday.net']='//*[@id="society"]/div[4]/div[2]/div[9]/div/div/div[1]/div[1]/article/div'
    ['www.chinatimes.com']='//*[@id="page-top"]/div/div[2]/div/div/article/div/div[1]/div[2]/div[2]/div[2]'
    ['udn.com']='/html/body/main/div/section[2]/section/article/div/section[1]'
    ['news.ltn.com.tw']='//*[@id="ltnRWD"]/div[10]/section/div[4]/div[2]'
    ['finance.ettoday.net']='//*[@id="finance"]/div[3]/div[2]/div[7]/div/div[1]/div[1]/div[2]/div[4]'
    ['ctee.com.tw']='//*[@id="post--24779"]/div[3]'
)
declare -A css_selector=(
    ['www.ettoday.net']='#society > div.wrapper_box > div.wrapper > div.container_box > div > div > div.c1 > div.part_area_1 > article > div > div.story'
    ['www.chinatimes.com']='#page-top > div > div:nth-child(2) > div > div > article > div > div:nth-child(2) > div.row > div.col-xl-11 > div.article-body'
    ['udn.com']='body > main > div > section.wrapper-left.main-content__wrapper > section > article > div > section.article-content__editor'
    ['news.ltn.com.tw']='#ltnRWD > div.content > section > div:nth-child(16) > div.text.boxTitle.boxText'
    ['finance.ettoday.net']='#finance > div.wrapper_box > div.wrapper > div.container_box > div > div.r1.clearfix > div.c1 > div.subject_article > div.story'
    ['ctee.com.tw']='div.entry-content.clearfix.single-post-content'
)

sys_prompt_1='你的任務是找到文章內容中存在的金融犯罪嫌疑公司與人物，並以輸出格式呈現，輸出內容包含犯罪人與公司，犯罪人與公司須以逗號分隔，並以「犯罪人與公司:」開頭，範例輸出格式如下：
### 輸出格式
犯罪主體: '
sys_prompt_2='你的任務是找到文章內容中指定的目標是否涉及犯罪，並以輸出格式呈現，輸出內容包含犯罪人與公司、刑責、刑責進度以及50字摘要。
犯罪主體: {{target}}
刑責: ：起訴、被告、控告、指控、罪嫌、搜索、提審、交保、扣押、收押、羈押、禁見、判刑、判決、改判無罪、不起訴、緩起訴
刑責進度: 侵害營業秘密、毒品販運、詐欺、詐騙、走私、稅務犯罪、組織犯罪、證券犯罪、貪污、貪瀆、舞弊、貪汙、賄賂、收賄、行賄、圖利、洗錢、賭博、簽賭、博弈、地下通匯、智慧財產犯罪、人口販運、性剝削、偽造貨幣、恐怖主義、資恐、非法販運武器、妨害自由、環保犯罪、偽造文書、仿冒、偽造、盜版、人頭戶、空殼公司、地下錢莊、販毒、吸金、地下通匯、內線交易、金融犯罪、舞弊、逃漏稅、洗錢、背信、不法所得、不法獲利、不法牟利、不法利益、詐領、違反銀行法 

範例輸出格式如下：
### 輸出格式
1. 犯罪主體: 
2. 刑責:
3. 刑責進度:
4. 摘要:'
usr_prompt="### 文章內容
$NEWS_CONTENT
"

extractor_result=$(submit "$sys_prompt_1" "$usr_prompt")
content=$(echo "$extractor_result" | sed 's/犯罪人與公司: //')
echo "$NEWS_URL,$content" >> outputs/output-instance-A.csv

echo "所有目標: $content"
delimiter=","

# Split the string into an array using awk
array=($(awk -F"$delimiter" '{for (i=1; i<=NF; i++) print $i}' <<< "$content"))

# Print the array elements
for element in "${array[@]}"; do
    echo "Target: $element"
    usr_prompt_2='###犯罪主體: '$element'\n\n'$usr_prompt
    echo $usr_prompt_2

    inferencer_result=$(submit "$sys_prompt_2" "$usr_prompt_2")
    # echo "Inferencer result: $inferencer_result"
    # Extract "犯罪人與公司"
    criminal_company=$(echo "$inferencer_result" | sed -n 's/^1\. 犯罪主體: \(.*\)$/\1/p')

    # Extract "刑責"
    criminal_penalty=$(echo "$inferencer_result" | sed -n 's/^2\. 刑責: \(.*\)$/\1/p')

    # Extract "刑責進度"
    criminal_progress=$(echo "$inferencer_result" | sed -n 's/^3\. 刑責進度: \(.*\)$/\1/p')

    # Extract "摘要"
    summary=$(echo "$inferencer_result" | sed -n 's/^4\. 摘要: \(.*\)$/\1/p')

    echo "主體: $criminal_company"
    echo "刑責: $criminal_penalty"
    echo "刑責進度: $criminal_progress"
    echo "摘要: $summary"

    echo "=========="

    csv_output="$NEWS_URL,$criminal_company,$criminal_penalty,$criminal_progress,$summary"
    # echo -n "$csv_output" >> output.csv
    echo "$csv_output" >> outputs/output-A.csv
done
# while IFS= read -r line; do
#     # news_url="$line"
# done < "news_source.txt"
