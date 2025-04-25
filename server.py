from flask import Flask, request, jsonify
from flask_cors import CORS
from LibraryDatabaseMY import Catalog, LogicalBook

app = Flask(__name__)
CORS(app)
catalog = Catalog()

@app.route('/books', methods=['GET'])
def sv_get_books():
    books = catalog.getCatalog()
    return jsonify([{
        'serialNumber': book[0],
        'title': book[1],
        'author': book[2],
        'copies': book[3]
    } for book in books])

@app.route('/books/<serial>', methods=['GET'])
def sv_get_book(serial):
    book = catalog.findBookBySerialNumber(serial)
    if book:
        return jsonify({
            'serialNumber': book[0][0],
            'title': book[0][1],
            'author': book[0][2],
            'copies': book[0][3]
        })
    return {'error': 'Book not found'}, 404

@app.route('/books', methods=['POST'])
def sv_add_book():
    data = request.get_json()
    new_book = LogicalBook(
        title=data['title'],
        author=data['author'],
        copies=data['copies'],
        serialNumber=data['serialNumber']
    )
    catalog.addBook(new_book)
    return {'message': 'Book added successfully'}, 201

@app.route('/books/<serial>', methods=['PUT'])
def sv_update_copies(serial):
    data = request.get_json()
    catalog.editBook(newTitle=data['title'], newAuthor=data['author'], SerialNumber=serial)
    return {'message': 'Book updated successfully'}

@app.route('/books/<serial>', methods=['DELETE'])
def sv_delete_book(serial):
    success = catalog.removeBook(serial)
    if success:
        return {'message': 'Book deleted successfully'}
    return {'error': 'Book not found'}, 404

@app.route('/api/checkout', methods=['POST'])
def sv_checkout_book():
    data = request.get_json()
    user_id = data['user_id']
    serial_number = data['serial_number']
    
    catalog.checkOutBook(user_id, serial_number)
    
    return jsonify({'message': 'Book checked out successfully'}), 200

@app.route('/users/<user_id>/books', methods=['GET'])
def sv_get_user_books(user_id):
    books = catalog.getUsersCheckedOutBooks(user_id)
    if books:
        return jsonify([{
            'checkout_id': book[0],
            'serialNumber': book[2],
            'checkout_date': book[3]
        } for book in books])
    return {'error': 'No books checked out'}, 404

@app.route('/')
def landing_page():
    return '''
        <html>
            <head>
                <title>Landing Page</title>
            </head>
            <body>
                <h1>Welcome!</h1>
                <p>This is a simple landing page for the server. If you are seeing this, that means the server is functional. You can now run the main application.</p>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)