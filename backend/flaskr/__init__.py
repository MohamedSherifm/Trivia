import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request , selection):
  page = request.args.get('page' , 1 , type = int)
  start = (page - 1) * QUESTIONS_PER_PAGE 
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

  
  


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  #CORS(app, resources={'/': {'origins': '*'}})
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers' , 'Content-Type,Authorization,true')
    response.headers.add('Access-COntrol-Allow-Methods' , 'GET , POST , PATCH , DELETE , OPTIONS ')
    return response

  
  @app.route('/categories')
  def get_all_gategories():
    categories = Category.query.all()
    categories_dict={}
    for i in categories:
      categories_dict[i.id] = i.type

    
    if len(categories)==0:
      abort(404)
    return jsonify({
      "success" : True,
      "categories" : categories_dict
    })  


  
  @app.route('/questions')
  def get_questions():
    #body = request.form.get('category')
    
    questions = Question.query.all()
     
    #questions = Question.query.filter(Question.category == tyty).all()  
    if len(questions)==0:
      abort(422)
    question = paginate_questions(request , questions)
    if len(question)==0:
      abort(404)
    current_category=[]
    
    for i in question:
      current_category.append(i.get('category'))
      
    categories = Category.query.all()

    cats={}
    for category in categories:
      cats[category.id] = category.type
    
    
    return jsonify({
      "success" : True ,
      "questions" : question,
      "total_questions" : len(questions),
      "categories":cats,
      "current_category": current_category}) 
    
    


  

  @app.route('/questions/<int:id>' , methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter(Question.id == id).one_or_none()
      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        "success":True,
        "question_id":question.id
      })
    except:
      abort(422)  


  

  @app.route('/questions' , methods=['POST'])
  def add_question():
    body = request.get_json()
    question_description = body.get('question')
    answer = body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')

    try :
      question = Question(question= question_description , answer = answer , difficulty = difficulty , category = category )
      question.insert()

      return jsonify({
      "success":True , 
      "new question":question.id
      })
    except:
      abort(422)      

  
  @app.route('/questions/search' , methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm')
    if search_term is None:
      abort(422)
    questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    
    
    all_questions = paginate_questions(request , questions)
    current_categories=[]
    for i in questions:
      current_categories.append(i.category)
    
    return jsonify({
      'success':True,
      'questions': all_questions,
      'total_questions':len(questions),
      'current_category':current_categories
    })  
    

  @app.route('/categories/<int:cat_id>/questions')
  def get_questions_based_on_category(cat_id):
    category = Category.query.filter_by(id = cat_id).all()
    if len(category)==0:
      abort(404)
    questions = Question.query.filter_by(category = category[0].id).all()
    current_questions = paginate_questions(request , questions)
    
    

    return jsonify({
      "success":True,
      "questions":current_questions,
      "total_questions" : len(questions),
      "current_category":category[0].type})



  
  @app.route('/quizzes' , methods = ['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions')
    category_selected = body.get('quiz_category')
    if (previous_questions is None) or (category_selected is None):
      abort (422)
    
    if (category_selected['id'] == 0) :
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category = category_selected['id']).all()

    
    
    def question_used(question):
       
      for i in previous_questions:
        if (i == question.id):
          return True
      return False   
      

    current_question = questions[random.randrange(0,len(questions),1)]  

    while (question_used(current_question)):
      current_question = questions[random.randrange(0,len(questions),1)]
      if (len(previous_questions)==len(questions)):
        return {
          'success':True,
          }
     
    
    return jsonify({
      "question": current_question.format(),
      "success" : True
    })  
  
    
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success":False,
      "error": 404,
      "message":"resource not found"

    }),404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success":False,
      "error" : 422 , 
      "message":"unprocessable"

    }),422
  return app

    