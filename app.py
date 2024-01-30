from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import psycopg

# app.config['JSON_AS_ASCII'] = False
# cors = CORS(app)
# if __name__ == '__main__':
#     app.run(debug=True)

# connection = psycopg.connect(
#     host='localhost',
#     dbname='todo',
#     user='postgres',
#     password='password',
# )

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)
if __name__ == '__main__':
    app.run(debug=True)

connection = psycopg.connect(
    host='localhost',
    dbname='todo',
    user='postgres',
    password='password',
)

@app.route('/todo-lists', methods=['POST'])
def post_todo_list():
    sql = '''
    SELECT ID
    FROM login;
    '''
    result = connection.execute(sql)
    key = [row[0] for row in result]
    
    new_key = 1
    while new_key in key:
        new_key += 1

    content = request.get_json()

    try:
        sql = '''
        INSERT INTO login (ID, loginID, password)
        VALUES
        (%(ID)s, %(LoginID)s, %(Password)s);
        '''
    # (%(ID)s, %(LoginID)s, %(Password)s);
        connection.execute(sql, {'ID': new_key, 'LoginID': content["LoginID"], 'Password': content["Password"]})
        connection.commit()  # トランザクションをコミット

        return jsonify({'message': 'created'})
    
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        connection.rollback()  # トランザクションのロールバック
        return jsonify({'message': 'error'})



# @app.route('/todo-lists', methods=['GET'])
# def get_todo_lists():
#     sql = '''
#     SELECT * FROM login;
#     '''
#     result = connection.execute(sql)
#     todo_lists = []
#     for row in result:
#         todo_list = {
#             'ID': row[0],
#             'LoginID' :row[1],
#             'Password': row[2]
#         }
#         todo_lists.append(todo_list)
#     return jsonify(todo_lists)


# @app.route('/todo-lists', methods=['POST'])
# def post_todo_list():

#     sql = '''
#     SELECT ID
#     FROM login;
#     '''
#     result = connection.execute(sql)
#     key = []
#     for row in result:
#         key.append(row[0])
#     new_key = 1
#     while True:
#         if new_key not in key:
#             break
#         new_key += 1
#     content = request.get_json()

#     try:
#         sql = '''
#         INSERT INTO login (ID, loginID, password)
#         VALUES
#         (%(ID)s, %(loginID)s, %(Password)s);
#         '''

#         connection.execute(sql, {'ID': new_key, 'LoginID': content["LoginID"], 'Password': content["Password"]})

#     except Exception:
#         connection.rollback()
#     else:
#         connection.commit()

#     return jsonify({'message': 'created'})




@app.route('/todo-lists/<int:id>', methods=['POST'])
def delete_todo_list(ID):
    try:
        sql = '''
        DELETE FROM login WHERE ID = %(id)s
        '''
        connection.execute(sql,{'id': id})
    except Exception:
        connection.rollback()
    else:
        connection.commit()

    return jsonify({'message': 'created'})

@app.route('/logs')
def get_logs():
    log_path = 'app.log'  # 実際のファイルパスに変更すること
    return send_file(log_path)