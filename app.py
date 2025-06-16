from flask import Flask,render_template,request
import pickle
import numpy as np

# Load the pickle files-------

books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('Similarity_score.pkl', 'rb'))
top_books = pickle.load(open('top_100_books.pkl', 'rb'))
users_and_books_pivot_table = pickle.load(open('users_and_books_pivot_table.pkl', 'rb'))
top_100_books_l = pickle.load(open('top_100_books_l.pkl', 'rb'))
top_100_books_s = pickle.load(open('top_100_books_s.pkl', 'rb'))

# instance of the class/ object creation
app = Flask(__name__)

# Render to the home page
@app.route('/')
def home():
    return render_template('home.html')

# Render to the books 
@app.route('/books')
def new():
    return render_template('all_books.html',
                    book_names = list(books['Book-Title'].values),
                    author_name = list(books['Book-Author'].values),
                    images = list(books['Image-URL-L'].values)
                    )

# Render to the top 100 books
@app.route('/top_100_books')
def index():
    return render_template('index.html',
                           book_name = list(top_books['Book-Title'].values),
                           author = list(top_books['Book-Author'].values),
                           image = list(top_100_books_l['Image-URL-L'].values),
                           votes = list(top_books['num_ratings'].values),
                           ratings = list(top_books['avg_ratings'].values)
                           )

# Render to the recommendation page
@app.route('/recommend')
def get_recommendation():
    return render_template('recommend_index.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(users_and_books_pivot_table.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])), key = lambda x : x[1], reverse = True)[1:6]

    recommended_books = []
    for i in similar_books:
        items = []
        temp_df = books[books['Book-Title'] == users_and_books_pivot_table.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

        recommended_books.append(items)

    print(recommended_books)

    return render_template('recommend_index.html',data=recommended_books)




if __name__  == '__main__':
    app.run(debug = True)

