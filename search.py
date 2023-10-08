import requests
import json
from operator import itemgetter

def stackoverflow_search(query, language=None, tag=None):
  """Searches Stack Overflow for the given query.

  Args:
    query: The search query.
    language: The programming language to filter the results by (optional).
    tag: The tag to filter the results by (optional).

  Returns:
    A list of Stack Overflow question objects, or an empty list if no results were found.
  """

  url = "https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={}&site=stackoverflow".format(query)

  if language is not None:
    url += "&tagged={}".format(language)

  if tag is not None:
    url += "&tagged={}".format(tag)

  response = requests.get(url)
  results = json.loads(response.content)

  questions = []
  for item in results["items"]:
    question = {
      "id": item["question_id"],
      "title": item["title"],
      "link": item["link"],
      "answer_count": item["answer_count"]
    }

    if "accepted_answer_id" in item:
      question["accepted_answer_id"] = item["accepted_answer_id"]
    else:
      question["accepted_answer_id"] = None

    if "score" in item:
      question["score"] = item["score"]
    else:
      question["score"] = 0

    questions.append(question)

  return questions

def sort_questions(questions):
  """Sorts the given list of Stack Overflow question objects by their score in descending order."""

  questions.sort(key=itemgetter("score"), reverse=True)

def paginate_questions(questions, page_size=10):
  """Paginates the given list of Stack Overflow question objects into pages of the given size.

  Args:
    questions: The list of Stack Overflow question objects to paginate.
    page_size: The size of each page (optional).

  Returns:
    A list of pages, where each page is a list of Stack Overflow question objects.
  """

  pages = []
  for i in range(0, len(questions), page_size):
    pages.append(questions[i:i + page_size])

  return pages

def main():
  """Searches Stack Overflow for the given query and displays the results to the user."""

  query = input("Enter a search query: ")
  language = input("Filter by language (optional): ")
  tag = input("Filter by tag (optional): ")

  questions = stackoverflow_search(query, language, tag)

  if not questions:
    print("No results found.")
    return

  sort_questions(questions)

  pages = paginate_questions(questions)

  current_page = 1
  while True:
    print("Page {} of {}".format(current_page, len(pages)))

    for question in pages[current_page - 1]:
      print("[{}] {} ({})".format(question["id"], question["title"], question["link"]))

    print("Enter a page number to view, or Q to quit: ")
    user_input = input()

    if user_input == "Q":
      break

    try:
      current_page = int(user_input)

      if current_page < 1 or current_page > len(pages):
        print("Invalid page number.")
    except ValueError:
      print("Please enter a valid page number.")

if __name__ == "__main__":
  main()
