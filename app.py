# pip install flask openai
# http://localhost:5000/daily_horoscope?zodiac_sign=aries

from flask import Flask, request, jsonify
import openai
import config

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# Route to generate horoscope
@app.route('/daily_horoscope', methods=['GET'])
def daily_horoscope():
    # Get zodiac sign from request parameters
    zodiac_sign = request.args.get('zodiac_sign')
    if not zodiac_sign:
        return jsonify({"error": "Please provide a zodiac sign."}), 400

    # Generate horoscope using OpenAI's API
    prompt = f"Provide a daily horoscope for {zodiac_sign}."
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an Astrologist."},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=100
        )
        horoscope = response.choices[0].message.content
        return jsonify({"zodiac_sign": zodiac_sign, "horoscope": horoscope})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)