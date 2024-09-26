from django.shortcuts import render , redirect
from .models import *
from .utils import *
import random
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

####################################################################################
def quiz_view(request):

    if 'quiz_questions' in request.session:
        quiz_questions = request.session['quiz_questions']
    else:
        level = request.session.get('level')
        subject = request.session.get('subject')
        num_questions = request.session.get('num_questions')

        if subject == "python" :
            if level == "beginner" :
                all_questions = python_easy()
            elif level == "intermediate" :
                all_questions = python_inter()
            elif level == "advance":
                all_questions = python_adv()
        elif subject == "java" : 
            if level == "beginner" :
                all_questions = java_easy()
            elif level == "intermediate" :
                all_questions = java_inter()
            elif level == "advance":
                all_questions = java_adv()


        # all_questions = python_easy()
        request.session['all_questions'] = all_questions
        quiz_questions = random.sample(all_questions, num_questions)
        request.session['quiz_questions'] = quiz_questions


        # all_questions = python_easy()
        # quiz_questions = random.sample(all_questions, num_questions)
        # request.session['quiz_questions'] = quiz_questions
        

    context = {
        'questions': quiz_questions
    }
    return render(request, 'ai-show.html', context)
####################################################################################

# def quiz_view(request):
#     # all_questions = load_questions()
#     # all_questions = python_easy()
#     # quiz_questions = random.sample(all_questions, 10)

#     if 'quiz_questions' in request.session:
#         quiz_questions = request.session['quiz_questions']
#     else:
#         all_questions = python_easy()
#         num_questions = request.session.get('num_questions')
#         quiz_questions = random.sample(all_questions, num_questions)
#         request.session['quiz_questions'] = quiz_questions

#     context = {
#         'questions': quiz_questions
#     }
#     return render(request, 'ai-show.html', context)
    # return render(request, 'quiz-v2.html', context)

####################################################################################

def ai_select(request):
    if 'quiz_questions' in request.session:
        del request.session['quiz_questions']

    if request.method == 'POST':
        subject = request.POST.get('subject')
        request.session['subject'] = str(subject)
        level = request.POST.get('level')
        request.session['level'] = str(level)
        num_questions = request.POST.get('num')
        if num_questions:
            try:
                num_questions = int(num_questions)
                request.session['num_questions'] = num_questions
                return redirect('ai_quiz')
            except ValueError:
                # Handle invalid integer conversion
                return HttpResponseBadRequest("Invalid number of questions")
        else:
            # Handle missing 'num' field
            return HttpResponseBadRequest("Number of questions not provided")

    return render(request, 'ai-generated.html')


# def ai_create_quiz(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         questions = request.POST.getlist('questions')
#         options = request.POST.getlist('options')
#         correct_options = request.POST.getlist('correct_options')
#         image_loc = request.POST.getlist('img')
#         quiz = Quiz.objects.create(title=title, host=request.user)
        
#         for i in range(len(questions)):
#             Question.objects.create(
#                 quiz=quiz,
#                 question_text=questions[i],
#                 option1=options[i*4],
#                 option2=options[i*4 + 1],
#                 option3=options[i*4 + 2],
#                 option4=options[i*4 + 3],
#                 correct_option=correct_options[i] ,
#                 image_loc=image_loc[i]
#             )
        
#         return redirect('quiz_detail', quiz_id=quiz.id)


def ai_create_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        questions = request.POST.getlist('questions')
        options = request.POST.getlist('options')
        correct_options = request.POST.getlist('correct_options')
        image_loc = request.POST.getlist('img')

        # Debugging information
        print(f"Title: {title}")
        print(f"Initial number of questions: {len(questions)}")
        print(f"Initial number of options: {len(options)}")
        print(f"Initial number of correct options: {len(correct_options)}")
        print(f"Initial number of image locations: {len(image_loc)}")

        # Filter out any deleted or empty questions
        filtered_questions = []
        filtered_options = []
        filtered_correct_options = []
        filtered_image_loc = []

        for i in range(len(questions)):
            if questions[i].strip():  # If the question is not empty
                filtered_questions.append(questions[i])
                filtered_correct_options.append(correct_options[i])

                # Extract corresponding options for this question
                filtered_options.extend(options[i * 4:(i + 1) * 4])
                if image_loc:
                    filtered_image_loc.append(image_loc[i] if i < len(image_loc) else None)

        # Debugging after filtering
        print(f"Filtered number of questions: {len(filtered_questions)}")
        print(f"Filtered number of options: {len(filtered_options)}")
        print(f"Filtered number of correct options: {len(filtered_correct_options)}")
        print(f"Filtered number of image locations: {len(filtered_image_loc)}")

        # Ensure filtered lists are consistent
        num_questions = len(filtered_questions)
        expected_options_length = num_questions * 4

        if len(filtered_options) != expected_options_length:
            return HttpResponseBadRequest("Mismatch in the number of options after filtering.")

        if len(filtered_correct_options) != num_questions:
            return HttpResponseBadRequest("Mismatch in the number of correct options after filtering.")

        if len(filtered_image_loc) != num_questions:
            return HttpResponseBadRequest("Mismatch in the number of images after filtering.")

        # Create the quiz
        quiz = Quiz.objects.create(title=title, host=request.user)

        for i in range(num_questions):
            Question.objects.create(
                quiz=quiz,
                question_text=filtered_questions[i],
                option1=filtered_options[i * 4],
                option2=filtered_options[i * 4 + 1],
                option3=filtered_options[i * 4 + 2],
                option4=filtered_options[i * 4 + 3],
                correct_option=filtered_correct_options[i],
                image_loc=filtered_image_loc[i] if filtered_image_loc else None
            )

        return redirect('quiz_detail', quiz_id=quiz.id)

    return HttpResponseBadRequest("Invalid request method.")





# def ai_create_quiz(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         questions = request.POST.getlist('questions')
#         options = request.POST.getlist('options')
#         correct_options = request.POST.getlist('correct_options')
#         image_loc = request.POST.getlist('img')

#         quiz = Quiz.objects.create(title=title, host=request.user)
        
#         for i in range(len(questions)):
#             option1 = options[i * 4] if i * 4 < len(options) else None
#             option2 = options[i * 4 + 1] if i * 4 + 1 < len(options) else None
#             option3 = options[i * 4 + 2] if i * 4 + 2 < len(options) else None
#             option4 = options[i * 4 + 3] if i * 4 + 3 < len(options) else None
#             correct_option = correct_options[i] if i < len(correct_options) else None
#             img = image_loc[i] if i < len(image_loc) else None

#             Question.objects.create(
#                 quiz=quiz,
#                 question_text=questions[i],
#                 option1=option1,
#                 option2=option2,
#                 option3=option3,
#                 option4=option4,
#                 correct_option=correct_option,
#                 image_loc=img
#             )
        
#         return redirect('quiz_detail', quiz_id=quiz.id)


# def ai_create_quiz(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         questions = request.POST.getlist('questions')
#         options = request.POST.getlist('options')
#         correct_options = request.POST.getlist('correct_options')
#         image_loc = request.POST.getlist('img')

#         quiz_questions = request.session.get('quiz_questions', [])

#         # Merge the posted questions with the session data
#         for i in range(len(questions)):
#             question_data = {
#                 'question': questions[i],
#                 'option1': options[i*4],
#                 'option2': options[i*4 + 1],
#                 'option3': options[i*4 + 2],
#                 'option4': options[i*4 + 3],
#                 'correct_option': correct_options[i],
#                 'image_loc': image_loc[i]
#             }
#             quiz_questions.append(question_data)

#         request.session['quiz_questions'] = quiz_questions

#         quiz = Quiz.objects.create(title=title, host=request.user)

#         # Save each question to the database
#         for question_data in quiz_questions:
#             Question.objects.create(
#                 quiz=quiz,
#                 question_text=question_data['question'],
#                 option1=question_data['option1'],
#                 option2=question_data['option2'],
#                 option3=question_data['option3'],
#                 option4=question_data['option4'],
#                 correct_option=question_data['correct_option'],
#                 image_loc=question_data['image_loc']
#             )
        
#         return redirect('quiz_detail', quiz_id=quiz.id)

    

# def quiz_add(request):

#     if request.method == 'post' :
#         level = request.session.get('level')
#         subject = request.session.get('subject')
#         num_questions = 1 

#         if subject == "python" :
#             if level == "beginner" :
#                 all_questions = python_easy()
#             elif level == "intermediate" :
#                 all_questions = python_inter()
#             elif level == "advance":
#                 all_questions = python_adv()

#         add_questions = random.sample(all_questions, num_questions)
#         request.session['add_questions'] = add_questions

#         data = {
#             'questions': add_questions
#         }
#         return JsonResponse(data)


def quiz_add(request):
    # Check if the request method is POST and if it's an AJAX request
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        level = request.session.get('level')
        subject = request.session.get('subject')
        num_questions = 1 

        # if subject == "python":
        #     if level == "beginner":
        #         all_questions = python_easy()
        #     elif level == "intermediate":
        #         all_questions = python_inter()
        #     elif level == "advance":
        #         all_questions = python_adv()
        #     else:
        #         return JsonResponse({'error': 'Invalid level'}, status=400)
        all_questions = request.session.get('all_questions')

        add_questions = random.sample(all_questions, num_questions)
        request.session['add_questions'] = add_questions

        # Prepare data to send back to JavaScript
        data = {
            'questions': add_questions
        }
        return JsonResponse(data)
        # else:
        #     return JsonResponse({'error': 'Invalid subject'}, status=400)

    # If the request method is not POST or it's not an AJAX request
    return HttpResponseBadRequest('Invalid request')





def remove_quiz_question(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        question_text = request.POST.get('question')
        quiz_questions = request.session.get('quiz_questions', [])
        
        # Filter out the question that needs to be removed
        updated_questions = [q for q in quiz_questions if q['question'] != question_text]
        request.session['quiz_questions'] = updated_questions
        
        return JsonResponse({'status': 'success'})
    return HttpResponseBadRequest('Invalid request')
