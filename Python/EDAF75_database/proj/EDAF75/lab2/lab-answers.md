# Question 4

1. Theaters have unique names, Is a username natural or is it only purpose to act as a unique identifier (? :o) 
2. Yes, a theatre may change it name. A user might, but we probably set the rules
3. Yes, performances
4. Maybe for the theatre table. The performances table might be easier to handle if it were to be indexed by an invented key. Same goes for most tables.

# Question 6
Relational Model:

* theatres(_th_name, capacity)
* movies(_title, _year, imdb_key, length)
* customers(_user_name, full_name, password)
* performances(_screen_date, _start_time, /_title/, /_year/, /_th_name/)
* tickets(_t_id, /th_name/, /title/, /year/, /screen_date/, /start_time/, /user_name/)


# Question 7
* Join performance with ticket and theatre, select capacity - count(ticket), save as a view
	- Upside, no need to keep track of it in db explicitly
	- Downside, need to sift through lots of data every time

* Store a counter? 
	- Downside, would need to be updated each time a ticket is inserted
	- How do we easily keep track of which counter to increment, if all tickets were related to the same performance, then we could do this with autoincrement. But they aren't, hence we need to implement logic for this on our own.
