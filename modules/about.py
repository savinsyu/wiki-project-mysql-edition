from flask import Blueprint, redirect, url_for, render_template, request, flash
from modules import connect

bp = Blueprint("about", __name__)

@bp.route("/about")
def about_list():
    conn = connect.get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM about")
            about_list_posts = cursor.fetchall()
    finally:
        conn.close()

    return render_template("about.html", about_list_posts=about_list_posts)


@bp.route("/add_about_name", methods=["GET", "POST"])
def add_about_name():
    if request.method == "POST":
        new_about_name = request.form.get("about_name", "").strip()

        if len(new_about_name) > 4:
            conn = connect.get_db_connection()
            try:
                with conn.cursor() as cursor:
                    # Для MySQL плейсхолдер — %s, а не ?
                    cursor.execute(
                        "INSERT INTO about (about_name) VALUES (%s)",
                        (new_about_name,)
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

            flash('Запись успешно добавлена!', category='success')
            return redirect(url_for("about.about_list"))
        else:
            flash('Ошибка сохранения записи, вы ввели мало символов!', category='danger')

    return render_template("about.html")
