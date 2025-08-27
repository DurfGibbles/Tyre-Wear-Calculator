from fastapi import FastAPI, Form, HTTPException
from mangum import Mangum
import pymysql
import os

app = FastAPI()

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('RDS_HOST', 'tyre-wear-db.c3uyg622u8ob.ap-southeast-2.rds.amazonaws.com'),
        user=os.environ.get('RDS_USER', 'admin'),
        password=os.environ.get('RDS_PASSWORD', 'Snapegaming193'),
        db=os.environ.get('RDS_DB', 'tyre_wear_calculator'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get('/')
async def serve_index():
    return {"message": "Redirect to S3 website", "url": "http://tyre-wear-calculator.s3-website-ap-southeast-2.amazonaws.com/index.html"}

@app.get('/results')
async def serve_results(result: str = "No results available."):
    return {"result": result}

@app.post('/submit')
async def handle_form(
    track_name: str = Form(...),
    lap_distance: float = Form(...),
    abrasiveness: int = Form(...),
    evolution: int = Form(...),
    car_name: str = Form(...),
    traction: int = Form(...),
    downforce: int = Form(...),
    braking_force: int = Form(...),
    tyre_name: str = Form(...)
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT base_wear FROM tyre WHERE tyre_name = %s', (tyre_name,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail=f"Tyre {tyre_name} not found")
        base_wear = result['base_wear']

        final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force

        cursor.execute(
            'INSERT INTO car (car_name, traction, downforce, braking) VALUES (%s, %s, %s, %s)',
            (car_name, traction, downforce, braking_force)
        )
        cursor.execute(
            'INSERT INTO track (track_name, distance, abrasiveness, evolution) VALUES (%s, %s, %s, %s)',
            (track_name, lap_distance, abrasiveness, evolution)
        )
        cursor.execute('INSERT INTO tyre_wear (final_wear) VALUES (%s)', (final_wear))

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Form submitted",
            "data": {
                "track_name": track_name,
                "lap_distance": lap_distance,
                "abrasiveness": abrasiveness,
                "evolution": evolution,
                "car_name": car_name,
                "traction": traction,
                "downforce": downforce,
                "braking_force": braking_force,
                "tyre_name": tyre_name
            },
            "result": f"Calculated tyre wear for {tyre_name}: {final_wear}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)