1.
(1)
git clone https://github.com/DJPmoney/Bee.git
git add 
git commit
git push -u origin master
(2)安裝套件:
python -m pip install --upgrade pip
pip install pandas
pip install requests
pip install progressbar2
(3)Eric 6 安裝套件:
pip install PyQt5
pip install QScintilla
(4)清除 local workspace 
git clean -dxf
git checkout -f
(5)sync tip code:
git fetch
git pull
(6) git add ignore
git add -A -f --ignore-errors 
(7) git branch 操作:
  -- 建立branch : git push origin master:[branch name]
  -- 刪除branch : git push origin :[branch name]
  -- merge branch : git merge [branch name]
  -- 複製 branch 中特定commit 至  local 端: git cherry-pick  [commit id]
  
2. Stock Data columm meanings
date - 日期
opening_price - 開盤價格
highest_price - 最高價格
lowest_price- 最低價格
finial_price- 收盤價格
quantity - 交易數量
short_buy - 融資
short_sell - 融卷
foreign_investment - 外資總張數
legal_person - 法人總張數
self_employed - 自營商總張數
avg_five -  5日線
avg_ten - 10日線價格
avg_twenty - 20日線價格
avg_sixty - 60日線價格
avg_hundred_twenty - 120日線價格

3. Company Revenue columm meanings:
date - 日期
revenue - 當月營收
last_month_revenue_percent - 上月比較%
last_year_revenue - 去年同月營收
last_year_revenue_percent - 去年同月增減%
accumulat_revenue - 當月累計營收
last_year_accumulat_revenue - 去年累計營收
revenue_percent - 前期比較%
