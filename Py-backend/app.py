from flask import Flask, request, jsonify
from flask_cors import CORS
from img2img import generate_image

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    negative_prompt = data.get('negativePrompt')
    base64_image_string = data.get('base64String')
    strength = data.get('strength')
    guidance_scale = data.get('guidance')
    output_img_name = data.get('outputImageName')

    clean_base64_image_string = base64_image_string.replace("data:image/jpeg;base64,", "")
    # print(prompt, negative_prompt, strength, guidance_scale, output_img_name)
    print(type(strength), type(guidance_scale))
    strength = float(strength)
    guidance_scale = float(guidance_scale)
    print(type(strength), type(guidance_scale))
    try:
        img_array = generate_image(prompt, negative_prompt, clean_base64_image_string, strength, guidance_scale, output_img_name)
        print(img_array)
        return jsonify({'images': img_array}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)