1.1
a. select game, install_source, count(distinct user_id) AS UniqueUsers, 
    sum(TOTAL_AMOUNT_SPENT) as TotalAmountSpent from gamers group by game, install_source;

b. select user_id, country, total_amount_spent from gamers where install_source = 'ua' 
    and total_amount_spent > 0 order by total_amount_spent desc limit 3;

c. select install_date, game, sum(total_amount_spent) / count(distinct user_id) as 
    DailyAverageRevenue from gamers group by install_date, game;

1.2

select t1.user_id, max(datediff(DAY, t1.Active_date, t2.Active_date) - 1) as max_gap from (
 select user_id, Active_date, row_number () over (partition by user_id order by Active_date) as rn
 from name_of_the_table) t1 left join (select user_id, Active_date, row_number () over (partition by user_id order by Active_date) as rn
  from name_of_the_table) t2 on t1.user_id = t2.user_id AND t1.rn = t2.rn – 1 group by t1.user_id;

