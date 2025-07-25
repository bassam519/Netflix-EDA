import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data Loading & Cleaning
movies = pd.read_csv('netflix_titles.csv')

# handle missing data
movies[['director','cast','country','date_added','rating','duration']] = \
movies[['director','cast','country','date_added','rating','duration']].fillna('Unknown')

# Convert date_added to datetime format
movies['date_added'] = pd.to_datetime(movies['date_added'], errors='coerce')

# Add year and column on date_added and release_year
movies['added_year'] = movies['date_added'].dt.year.astype('Int64')
movies['added_month'] = movies['date_added'].dt.month.astype('Int64')

# Number of shows added each year
num_show_per_year = movies.groupby('added_year')['show_id'].count()

# plot the num_show_per_year
plt.figure(1)
plt.bar(num_show_per_year.index,num_show_per_year.values)
plt.title('Number of Netflix Shows Added Each Year')
plt.xlabel('Added Year')
plt.ylabel('Number of shows added each year')
plt.tight_layout()

# Number of shows per country (top 10)
top_countries  = movies[movies['country'] != 'Unknown'].groupby('country')['show_id'].count().sort_values(ascending=False)
top_countries = top_countries .head(10)

# plot top_countries 
plt.figure(2)
plt.barh(top_countries.index,top_countries.values,color='teal')
plt.title('Top 10 Countries by Number of Netflix Shows')
plt.xlabel('Number of Shows')
plt.ylabel('Country')
plt.tight_layout()

# Duration statistics (mean, min, max)
movies_only = movies[movies['type'] == 'Movie'].copy() # filter only movies
movies_only = movies_only.dropna(subset=['duration'])
movies_only['duration'] = movies_only['duration'].str.extract('(\d+)').astype(float)  # Extract number from duration of movies
movies_only = movies_only.dropna(subset=['duration'])
duration_statistics=movies_only['duration']
# plot
plt.figure(3)
plt.title('Movie Duration Distribution')
plt.ylabel('Duration (minutes)')
plt.boxplot(duration_statistics)

# Total number of shows, [movies vs TV] shows count
type_counts = movies['type'].value_counts()

# plot
plt.figure(4)
plt.bar(type_counts.index,type_counts.values)
plt.title('Number of Movies vs TV Shows on Netflix')
plt.xlabel('Type')
plt.ylabel('Count')
plt.tight_layout()

# Filter shows by genre[listed_in] ->["Drama" and 'Comedy]
drama_genre = movies[movies['listed_in'].str.contains("Drama")].shape[0]
comedy_genre = movies[movies['listed_in'].str.contains("Comedy")].shape[0]
genre=['Drama','Comedy']
number_of_shows =[drama_genre,comedy_genre]

# plot
plt.figure(5)
plt.barh(genre,number_of_shows,color=['skyblue','steelblue'])
plt.title('Number of Drama and Comedy Shows on Netflix')
plt.xlabel('Genre')
plt.ylabel('Number of shows')
plt.tight_layout()

# Filter by country ("India" and "United States")
unitedstates=movies[movies['country'] == 'United States'].shape[0]
india=movies[movies['country'] == 'India'].shape[0]
countries=['United States','India']
countries_shows_count=[unitedstates,india]

# plot
plt.figure(6)
plt.bar(countries,countries_shows_count,color='skyblue')
plt.title('Netflix Content by Country')
plt.xlabel("Country")
plt.ylabel("Number of Shows")
plt.tight_layout()

# Shows Added by Year (Recent 5 Years)
added_last_5_years=movies[movies['added_year'] >= 2017].groupby('added_year')['show_id'].count()
colors = ['#008080', '#FF6F61', '#FFD700', '#708090', '#87CEEB']
# plot
plt.figure(7)
plt.pie(added_last_5_years.values,labels=None,autopct='%.2f%%', colors=colors,textprops={'color': 'white', 'weight': 'bold', 'fontsize': 12})
plt.legend(added_last_5_years.index)
plt.tight_layout()

# Distribution of Content Ratings (Top 5)
unique_ratings,counts = np.unique(movies['rating'],return_counts=True)

# sort indices by count
sorted_indices = np.argsort(counts)[::-1]
top_ratings = unique_ratings[sorted_indices][:5]
top_counts = counts[sorted_indices][:5]

# plot
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#FFA07A', '#20B2AA']
plt.figure(8)
plt.pie(top_counts, labels=top_ratings, autopct='%.2f%%', colors=colors,textprops={'color': 'white', 'weight': 'bold', 'fontsize': 12})
plt.title('Top 5 Netflix Ratings')
plt.legend()
plt.tight_layout()
plt.show()