from flask import Flask, request, Response
import sqlite3
import json

app = Flask(__name__)

def rows_to_ordered_dicts(cursor, rows):
    columns = [col[0] for col in cursor.description]
    result = []
    for row in rows:
        result.append({columns[i]: row[i] for i in range(len(columns))})
    return result

def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        status=status,
        mimetype='application/json'
    )

def get_data(sql, prm):
    conn = sqlite3.connect('premier_league.db')
    cursor = conn.cursor()
    cursor.execute(sql, (f"%{prm}%",))
    rows = cursor.fetchall()
    if rows:
        data = rows_to_ordered_dicts(cursor, rows)
        conn.close()
        return json_response(data)
    else:
        conn.close()
        return json_response({"message": "Không tìm thấy"}, 404)

# API tra cứu theo tên cầu thủ
@app.route('/player', methods=['GET'])
def get_player_by_name():
    name = request.args.get('name')
    if not name:
        return json_response({"error": "Vui lòng cung cấp tên cầu thủ ?name="}, 400)
    sql = "SELECT * FROM premier_league_stats WHERE Player LIKE ?"
    return get_data(sql, name)

# API tra cứu theo câu lạc bộ
@app.route('/club', methods=['GET'])
def get_players_by_club():
    club = request.args.get('club')
    if not club:
        return json_response({"error": "Vui lòng cung cấp tên câu lạc bộ ?club="}, 400)
    sql = "SELECT * FROM premier_league_stats WHERE Squad LIKE ?"
    return get_data(sql, club)

if __name__ == '__main__':
    app.run(debug=True)