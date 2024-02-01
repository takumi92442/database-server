from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import psycopg

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

@app.route('/login', methods=['GET'])
def get_Login():
    sql = '''
    SELECT * FROM login;
    '''
    result = connection.execute(sql)
    login_list = []
    for row in result:
        login = {
            'LoginID' :row[0],
            'Password': row[1]
        }
        login_list.append(login)
    return jsonify(login_list)


@app.route('/login', methods=['POST'])
def post_Login():

    content = request.get_json()

    try:
        sql = '''
        INSERT INTO login (loginID, password)
        VALUES
        (%(LoginID)s, %(Password)s);
        '''
        connection.execute(sql, {'LoginID': content["LoginID"], 'Password': content["Password"]})
        connection.commit()  # トランザクションをコミット

        return jsonify({'message': 'created'})
    
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        connection.rollback()  # トランザクションのロールバック
        return jsonify({'message': 'error'})



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




# @app.route('/login', methods=['POST'])
# def post_login():
#     sql = '''
#     SELECT ID
#     FROM login;
#     '''
#     result = connection.execute(sql)
#     key = [row[0] for row in result]
    
#     new_key = 1
#     while new_key in key:
#         new_key += 1

#     content = request.get_json()

#     try:
#         sql = '''
#         INSERT INTO login (ID, loginID, password)
#         VALUES
#         (%(ID)s, %(LoginID)s, %(Password)s);
#         '''
#         connection.execute(sql, {'ID': new_key, 'LoginID': content["LoginID"], 'Password': content["Password"]})
#         connection.commit()  # トランザクションをコミット

#         return jsonify({'message': 'created'})
    
#     except Exception as e:
#         app.logger.error(f"An error occurred: {e}")
#         connection.rollback()  # トランザクションのロールバック
#         return jsonify({'message': 'error'})


@app.route('/task_list', methods=['GET'])
def get_task_list():

    sql = '''
    SELECT * FROM task_list;
    '''
    result = connection.execute(sql)
    task_list = []
    for row in result:
        task = {
            'ID' :row[0],
            'LoginId': row[1],
            'Task':row[2],
            'LimitDate':row[3]
        }
        task_list.append(task)
    return jsonify(task_list)




@app.route('/task_list', methods=['POST'])
def post_task_list():
    sql = '''
    SELECT ID
    FROM task_list;
    '''
    result = connection.execute(sql)
    key = [row[0] for row in result]
    
    new_key = 1
    while new_key in key:
        new_key += 1

    content = request.get_json()
    print(content)

    try:
        sql = '''
        INSERT INTO task_list (ID, LoginID, Task, LimitDate)
        VALUES (%(ID)s, %(LoginID)s, %(Task)s, %(LimitDate)s);
        '''

        connection.execute(sql, {'ID':new_key,'LoginID': content["LoginID"], 'Task':content["Task"], "LimitDate" :content["LimitDate"]})
        connection.commit()  # トランザクションをコミット


        return jsonify({'message': 'created'})
    
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        connection.rollback()  # トランザクションのロールバック
        return jsonify({'message': 'error'})