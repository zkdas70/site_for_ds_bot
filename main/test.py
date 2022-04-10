# from requests import get
#
#
# print(get('http://127.0.0.1:5000/api/news').json())
# print(get('http://localhost:5000/api/news/1').json())
# print(get('http://localhost:5000/api/news/999').json())
# print(get('http://localhost:5000/api/news/q').json())


# @app.route('/news', methods=['GET', 'POST'])
# @login_required
# def add_news():
#     form = NewsForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = News()
#         news.title = form.title.data
#         news.content = form.content.data
#         news.is_private = form.is_private.data
#         current_user.news.append(news)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect('/')
#     return render_template('news.html', title='Добавление новости',
#                            form=form)


# @app.route('/news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     form = NewsForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         news = db_sess.query(News).filter(News.id == id,
#                                           News.user == current_user
#                                           ).first()
#         if news:
#             form.title.data = news.title
#             form.content.data = news.content
#             form.is_private.data = news.is_private
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = db_sess.query(News).filter(News.id == id,
#                                           News.user == current_user
#                                           ).first()
#         if news:
#             news.title = form.title.data
#             news.content = form.content.data
#             news.is_private = form.is_private.data
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     return render_template('news.html',
#                            title='Редактирование новости',
#                            form=form
#                            )


# @app.route('/news_delete/<int:id>')
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.id == id,
#                                       News.user == current_user
#                                       ).first()
#     if news:
#         db_sess.delete(news)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')
serv = {'test': 0.0, 'te2st': 0.0}
for i in serv:
    print(i, serv[i])
