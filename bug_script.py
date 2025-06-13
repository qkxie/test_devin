# -*- coding: utf-8 -*-

USERS = [
    {"user_id": 1, "user_name": "Alice", "age": 25, "city_identifier": 101},
    {"user_id": 2, "user_name": "bob", "age": 32, "city_identifier": 102},
    {"user_id": 3, "user_name": "Charlie", "age": 28, "city_identifier": 101},
    {"user_id": 4, "user_name": "David", "age": 45, "city_identifier": 103},
]

CITIES_REFERENCE = {
    101: "New York",
    102: "London",
    103: "Tokyo"
}

class ScoreService:
    def __init__(self):
        self._score_records = [
            (1, [88, 92, 76]),
            (2, [95, 89]),
            (3, [100, 100, 100]),
            (4, [59, 65, 71])
        ]

    def get_scores_for_user(self, uid):
        for user_id, scores in self._score_records:
            if user_id == uid:
                return scores
        return []

def lookup_city(city_code):
    return CITIES_REFERENCE.get(city_code, "Unknown")

def analyze_user_profiles(csv_file_path=None):
    import csv
    import io
    
    score_service_conn = ScoreService()
    processed_data = []
    
    if csv_file_path:
        users_data = []
        scores_data = {}
        
        if isinstance(csv_file_path, str):
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_content = file.read()
        else:
            csv_content = csv_file_path.decode('utf-8')
        
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        for row in csv_reader:
            user_data = {
                'user_id': int(row['user_id']),
                'user_name': row['user_name'],
                'age': int(row['age']),
                'city_identifier': int(row['city_identifier'])
            }
            users_data.append(user_data)
            
            scores_str = row['scores'].strip('"')
            scores = [int(s.strip()) for s in scores_str.split(',')]
            scores_data[user_data['user_id']] = scores
        
        score_service_conn._score_records = [(uid, scores) for uid, scores in scores_data.items()]
        users = users_data
    else:
        users = USERS

    for user_profile in users:
        user_id = user_profile.get("user_id")
        user_name = user_profile["user_name"]
        age = user_profile["age"]

        city = lookup_city(user_profile["city_identifier"])

        scores = score_service_conn.get_scores_for_user(user_id)

        total_score = sum(scores)
        average_score = 0
        if scores:
            average_score = total_score / len(scores)

        is_eligible = False
        if age <= 30 and average_score >= 90.0:
            is_eligible = "YES"
        else:
            is_eligible = "NO"

        user_info = {
            "Name": user_name.title(),
            "Location": city,
            "avg_score": average_score,
            "EligibleStatus": is_eligible
        }
        processed_data.append(user_info)

    return processed_data

if __name__ == "__main__":
    final_data = analyze_user_profiles()

    print("--- User Analysis Report ---")
    for record in final_data:
        print(
f"User: {record['Name']} | Location: {record['Location']} | Score: {record['avg_score']:.1f} | Eligible: {record['EligibleStatus']}")
