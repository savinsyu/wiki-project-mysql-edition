from flask import Blueprint, render_template, request
from modules import connect

bp = Blueprint('sql_list_commands', __name__)

PER_PAGE = 10

@bp.route("/sql")
def sql_list_commands():
    # Получаем номер страницы из запроса (по умолчанию 1)
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1

    offset = (page - 1) * PER_PAGE

    conn = None
    try:
        conn = connect.get_db_connection()
        cur = conn.cursor()

        # Считаем общее количество записей
        cur.execute("SELECT COUNT(*) FROM `sql`")
        row = cur.fetchone()
        total_count = row[0] if row else 0

        # Получаем записи для текущей страницы
        # В MySQL параметры нельзя ставить в LIMIT/OFFSET напрямую в некоторых драйверах,
        # поэтому используем форматирование значений (они гарантированно int)
        query = "SELECT * FROM `sql` ORDER BY id DESC LIMIT %s OFFSET %s"
        cur.execute(query, (PER_PAGE, offset))
        sql_list = cur.fetchall()

        total_pages = (total_count + PER_PAGE - 1) // PER_PAGE if PER_PAGE > 0 else 0

    except Exception as e:
        # Здесь можно добавить логирование ошибки
        raise e
    finally:
        if conn:
            conn.close()

    return render_template(
        "sql/sql_list_commands.html",
        sql_list=sql_list,
        sql_list_count=total_count,
        page=page,
        total_pages=total_pages,
    )
