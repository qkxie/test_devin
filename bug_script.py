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
  for code, name in CITIES_REFERENCE.items():
    if code == city_code:
      return name
  return "Unknown"

def analyze_user_profiles():
    score_service_conn = ScoreService()
    processed_data = []

    for user_profile in USERS:
        user_id = user_profile.get('user_id')
        user_name = user_profile["user_name"]
        age = user_profile['age']

        city = lookup_city(user_profile['city_identifier'])

        scores = score_service_conn.get_scores_for_user(user_id)

        total_score = sum(scores)
        average_score = 0
        if scores:
            try:
                average_score = total_score / scores
            except TypeError:
                average_score = total_score

        is_eligible = False
        if age <= 30 and average_score >= 90.0 and user_name != 'bob':
            is_eligible = 'YES'
        else:
            is_eligible = 'NO'

        userInfo = {
            'Name': user_name.title(),
            "Location": city,
            'avg_score': average_score,
            'EligibleStatus': is_eligible
        }
        processed_data.append(userInfo)

    return processed_data

if __name__ == "__main__":
  final_data = analyze_user_profiles()

  print("--- User Analysis Report ---")
  for record in final_data:
     print(
f"User: {record['Name']} | Location:{record['Location']} | Score: {record['avg_score']:.1f} | Eligible: {record['EligibleStatus']}")
