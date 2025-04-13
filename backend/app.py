from flask import Flask, request, jsonify
import redis
import time
import os
import mysql.connector
import json
import threading

app = Flask(__name__)

# Redis connection settings
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_password = os.environ.get('REDIS_PASSWORD', None)

# Create a Redis connection pool
redis_pool = redis.ConnectionPool(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True,  # Automatically decode responses to UTF-8
    max_connections=10      # Limit maximum connections
)

# Function to get a Redis client from the pool
def get_redis_client():
    return redis.Redis(connection_pool=redis_pool)

# Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'user'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'messages_db')
    )

# Process messages from Redis and store them in MySQL
def process_messages():
    print("Message processor started...")
    while True:
        redis_client = None
        try:
            # Get a fresh Redis client for each iteration
            redis_client = get_redis_client()
            
            # Get message from Redis queue (blocking with timeout)
            message_data = redis_client.blpop('message_queue', timeout=1)
            
            if message_data:
                queue_name, message_str = message_data
                try:
                    message_json = json.loads(message_str)
                    message_text = message_json.get('message', '')
                    
                    print(f"Processing message: {message_text}")
                    
                    # Store in MySQL
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute(
                        "INSERT INTO messages (message, timestamp) VALUES (%s, NOW())",
                        (message_text,)
                    )
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    print(f"Stored message in database: {message_text}")
                except Exception as e:
                    print(f"Error processing message: {e}")
        except Exception as e:
            print(f"Error in message processor: {e}")
            time.sleep(1)  # Avoid tight loop in case of connection issues

# API endpoint to receive messages
@app.route('/message', methods=['POST'])
def receive_message():
    redis_client = None
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'status': 'error', 'message': 'No message provided'}), 400
        
        # Get a fresh Redis client for this request
        redis_client = get_redis_client()
        
        # Add message to Redis queue
        redis_client.rpush('message_queue', json.dumps({'message': message}))
        
        return jsonify({'status': 'success', 'message': 'Message received'})
    except Exception as e:
        print(f"Error in receive_message: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    # Check Redis connection
    redis_status = "OK"
    try:
        client = get_redis_client()
        client.ping()
    except Exception as e:
        redis_status = f"Error: {str(e)}"
    
    # Check DB connection
    db_status = "OK"
    try:
        conn = get_db_connection()
        conn.close()
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    return jsonify({
        'status': 'healthy' if redis_status == "OK" and db_status == "OK" else "unhealthy",
        'redis': redis_status,
        'database': db_status
    })

if __name__ == '__main__':
    # Start message processor in a separate thread
    processor_thread = threading.Thread(target=process_messages, daemon=True)
    processor_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
