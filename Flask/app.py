from flask import Flask,request,render_template,redirect,flash,url_for
import os
import sys
app = Flask(__name__)
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing  import image
import numpy as np
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '545454'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads')

detail = {"French fries": ["Total time: 50 minutes", "Preparation time: 20 minutes", "Calories: 520"],
          "Pizza": ["Total time: 20 minutes", "Preparation time: 10 minutes", "Calories: 744"],
          "Samosa": ["Total time: 1 hour", "Preparation time: 25 minutes", "Calories: 575"]}

detail_1 = {"French fries": ["Chop the potatoes",
                             "Soak cut potatoes in ice-cold water for 10-15 minutes",
                             "Deep fry the potato fries",
                             "Sprinkle salt and pepper and serve hot"],
            "Pizza": ["Prepare the pizza dough",
                      "Prepare the pizza base",
                      "Chop all the vegetables for the pizza",
                      "Spread the sauce and veggies on the base",
                      "Bake the pizza at 250 degree Celsius for 10 minutes"],
            "Samosa": ["Sauté cumin seeds for potato filling",
                       "Add spices and boiled potatoes and cook for a while",
                       "Prepare the dough for the Samosa",
                       "Roll the dough in small puris and cut into half",
                       "Fill the semi-circle with potato filling and deep fry"]

            }

detail_2 = {"French fries": ["500 gm potatoes", "2 cup refined oil", "Salt", "Black pepper"],
            "Pizza": ["2 cup all purpose flour", "100 ml tomato ketchup", "1 tomato", "2 onion",
                      "1 teaspoon chilli flakes", "1 teaspoon baking powder", "1 teaspoon sugar",
                      "100 gm processed cheese", "4 mushroom", "1/2 capsicum (green pepper)",
                      "1 teaspoon oregano", "1/2 cup mozzarella", "1 tablespoon dry yeast"],
            "Samosa": ["2 cup all purpose flour", "1 teaspoon cumin seeds", "1 teaspoon crushed ginger",
                       "1 teaspoon crushed ginger", "1 teaspoon raisins", "5 boiled potato",
                       "1 teaspoon coriander powder", "1 teaspoon red chilli powder",
                       "1 teaspoon kasoori methi leaves",
                       "1 teaspoon carom seeds", "1/4 cup water", "2 cup refined oil",
                       "1/2 teaspoon coriander seeds",
                       "1 teaspoon green chilli", "1 teaspoon cashews", "1 teaspoon cumin powder",
                       "1/2 teaspoon garam masala powder", "salt as required", "1 teaspoon coriander leaves",
                       "2 tablespoon ghee", "1 handful raw peanuts", ]
            }

detail_3 = {"French fries": [
    "To prepare this easy recipe, you need to make sure that they are cut in the right shape and size. They should neither be too thick, nor too thin and should be cut clean and sharp. The trick is to first slice the potatoes and then cut them lengthwise. You can also use a fries cutter for that long, even shape.",
    "Now, wash the potatoes under running water till they are squeaky clean. Place them in a bowl of iced water for 10 to 15 minutes. Keep them submerged in water or they will turn black.",
    "Now, heat the oil in a deep bottomed pan. Once the smoke starts appearing, reduce the flame and allow it to acquire a lower temperature. Now, deep fry the potatoes in batches. Keep the flame low. This will make them crunchy and also help retain their colour.",
    "Drain excess oil and place them on an absorbent paper. Allow them to cool. Now sprinkle salt and pepper and toss well. Serve immediately with ketchup. They can also be served with burgers and cutlets."],
    "Pizza": [
        "Take a dough kneading plate and add all-purpose flour to it. Next, add salt and baking powder in it and sieve the flour once. Then, make a well in the centre and add 1 teaspoon of oil to it. On the other hand, take a little warm water and mix the yeast in it along with 1 teaspoon of sugar. Mix well and keep aside for 10-15 minutes. The yeast will rise in the meantime. Once the yeast has risen, add it to the flour knead the dough nicely using some water. Keep this dough aside for 4-6 hours. Then knead the dough once again. Now, the pizza dough is ready.",
        "Preheat the oven at 180 degree Celsius. Now, is the time to make the pizza base when the dough is ready. Dust the space a little using dry flour and take a large amount of the pizza dough. Using a rolling pin, roll this dough into a nice circular base. (Note: Make sure that the circular base is even at all ends.) Once you have made the base, use a fork and prick the base with it so that the base doesn't rise and gets baked nicely. Put it into the preheated oven and bake it 10 minutes. Now, your pizza base is ready.",
        "Now, wash the capsicum and slice it thinly in a bowl. Then, peel the onions and cut thin slices of it as well in another bowl. And finally, cut tomatoes and mushrooms in the same manner. However, make sure that those tomatoes have less juice in them. Once all the veggies are done, Now, grate the processed and mozzarella cheese in separate bowls.",
        "Then, take the fresh pizza base and apply tomato ketchup all over. Spread half the processed cheese all over the base and evenly put the veggies all across the base. Once you have put all the veggies, put a thick layer of mozzarella cheese.",
        "Put this pizza base in a baking tray and place it inside the oven. Let the pizza bake 10 minutes at 250 degree Celsius. Once done, take out the baking tray and slice the pizza. Sprinkle oregano and chilli flakes as per your taste and serve hot. (Note: Make sure that the oven is preheated at 250 degree Celsius for 5 minutes at least.)"],
    "Samosa": [
        "To make delicious samosas at home, first, make the filling. Put a pan on medium flame and add 2 tsp oil in it. Once the oil is hot enough, add cumin seeds and allow them to crackle.",
        "Now, add whole coriander seeds, ginger and green chilli. Saute for a minute and then add chopped cashews and raisins, peanuts if you like them, boiled and mashed potatoes, cumin powder, coriander powder, garam masala powder, red chilli powder, salt to taste, kasoori methi leaves, coriander leaves. Mix well and saute for 2 minutes. Your stuffing is ready!",
        "Now, to prepare the dough, take a mixing bowl and combine all-purpose flour along with carom seeds and salt. Mix and then add ghee and start kneading by adding a little water at a time. Ensure that you add water gradually and make a firm dough. A soft dough will not make your samosas crispy. Cover the dough with a damp muslin cloth and keep aside for about half an hour.",
        "Once done, roll out few small-sized balls from the dough. Flatten them further with the help of your palms and then with a rolling pin. Give them a round shape and cut in half. Now dip your hands in water, fold the edges of the semi-circle in order to give it a cone shape.",
        "Take the filling with the help of a spoon and stuff it in the cone. Seal the ends properly by pressing the edges lightly with your fingers. Then, heat oil in a pan and deep fry the samosas on low heat until they turn golden brown and crispy. Serve with tomato ketchup and green chutney. Enjoy it as a tea-time snack!"]
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=["POST","GET"])
def start():
    for f in os.listdir('static/uploads'):
        if f.endswith('.jpg'):
            os.remove(os.path.join('static/uploads', f))

    filename=""
    prediction=""
    path_local=""
    r_file=""
    n1,n2=0,0
    h_path=""
    width=0
    height=0

    if request.method == "POST":
        file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            path_local = app.config['UPLOADED_PHOTOS_DEST'] + "/" + filename
            sucess=True
            r_file="static/uploads/"+filename
            model = load_model("recipe_best_2.h5")
            img = image.load_img(r_file,target_size = (224,224))
            x = image.img_to_array(img)
            x = np.expand_dims(x,axis = 0)
            pred = np.argmax(model.predict(x))
            index = ["French fries","Pizza","Samosa"]
            prediction = index[pred]
            print(pred)
            h_path="static/uploads/"+filename
            n1=len(detail[prediction])
            n2=len(detail_1[prediction])
            # filename=filename.strip(".jpg")


        else:
            success = False

    return render_template("index.html", file=h_path,prediction=prediction,detail=detail,detail_1=detail_1,n1=n1,n2=n2,filename=filename)


@app.route('/info/<prediction>/<file>',methods=["POST","GET"])
def info(prediction,file):
    prediction=prediction
    t_file=file

    n3 = len(detail_2[prediction])
    n4= len(detail_3[prediction])
    return render_template("info.html",prediction=prediction,file=t_file,detail_3=detail_3,detail_2=detail_2,n3=n3,n4=n4,detail_1=detail_1)


if __name__ == '__main__':
    app.run(debug=True)