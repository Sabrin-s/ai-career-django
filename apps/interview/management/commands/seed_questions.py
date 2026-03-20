from django.core.management.base import BaseCommand
from apps.interview.models import QuestionBank

QUESTIONS = [
    {'category': 'python', 'difficulty': 'easy',
     'question': 'What is the difference between a list and a tuple in Python?',
     'expected_keywords': ['mutable', 'immutable', 'list', 'tuple', 'ordered'],
     'sample_answer': 'A list is mutable (can be changed) while a tuple is immutable (cannot be changed). Lists use [], tuples use (). Tuples are hashable and can be used as dictionary keys.'},
    {'category': 'python', 'difficulty': 'medium',
     'question': 'Explain decorators in Python with an example.',
     'expected_keywords': ['decorator', 'function', 'wrapper', 'higher-order', 'closure'],
     'sample_answer': 'A decorator is a higher-order function that wraps another function to extend its behaviour without modifying it. Using the @ syntax before a function definition applies the decorator.'},
    {'category': 'python', 'difficulty': 'hard',
     'question': 'Explain Python\'s GIL and its impact on multi-threading.',
     'expected_keywords': ['GIL', 'thread', 'CPython', 'concurrency', 'multiprocessing'],
     'sample_answer': 'The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time. For CPU-bound tasks, use multiprocessing to bypass it. For I/O-bound tasks, threading still works well.'},
    {'category': 'django', 'difficulty': 'easy',
     'question': 'What is the purpose of Django\'s ORM?',
     'expected_keywords': ['ORM', 'database', 'model', 'query', 'SQL', 'abstraction'],
     'sample_answer': 'Django ORM lets you interact with the database using Python objects instead of raw SQL. You define models as Python classes and Django translates operations into SQL automatically.'},
    {'category': 'django', 'difficulty': 'medium',
     'question': 'Explain Django middleware and give a use case.',
     'expected_keywords': ['middleware', 'request', 'response', 'pipeline', 'authentication'],
     'sample_answer': 'Middleware is a hook into Django request/response processing. Each component processes the request before the view and response after. Common uses include authentication, logging, and CORS headers.'},
    {'category': 'django', 'difficulty': 'hard',
     'question': 'How would you optimise a slow Django queryset?',
     'expected_keywords': ['select_related', 'prefetch_related', 'N+1', 'index', 'only', 'defer'],
     'sample_answer': 'Fix N+1 problems with select_related and prefetch_related. Use only() or defer() to fetch required fields. Add database indexes on filtered columns. Cache repeated queries with Redis.'},
    {'category': 'sql', 'difficulty': 'easy',
     'question': 'What is the difference between INNER JOIN and LEFT JOIN?',
     'expected_keywords': ['inner join', 'left join', 'match', 'null', 'rows'],
     'sample_answer': 'INNER JOIN returns only rows where there is a match in both tables. LEFT JOIN returns all rows from the left table and matched rows from the right; unmatched right side columns are NULL.'},
    {'category': 'sql', 'difficulty': 'medium',
     'question': 'What are indexes in MySQL and how do they improve performance?',
     'expected_keywords': ['index', 'B-tree', 'query', 'performance', 'WHERE'],
     'sample_answer': 'An index is a B-tree data structure that allows MySQL to find rows quickly without scanning the entire table. The trade-off is slightly slower writes because indexes must be updated on INSERT/UPDATE/DELETE.'},
    {'category': 'javascript', 'difficulty': 'easy',
     'question': 'What is the difference between var, let, and const?',
     'expected_keywords': ['var', 'let', 'const', 'scope', 'hoisting', 'block', 'function'],
     'sample_answer': 'var is function-scoped and hoisted. let is block-scoped and not hoisted. const is block-scoped, not hoisted, and cannot be reassigned. Use const by default, let when you need to reassign.'},
    {'category': 'javascript', 'difficulty': 'medium',
     'question': 'Explain promises and async/await in JavaScript.',
     'expected_keywords': ['promise', 'async', 'await', 'asynchronous', 'resolve', 'reject', 'callback'],
     'sample_answer': 'A Promise represents a value that will be available in the future. async/await is syntactic sugar over promises making async code look synchronous. await pauses execution until the promise resolves.'},
    {'category': 'system_design', 'difficulty': 'medium',
     'question': 'How would you design a URL shortener like bit.ly?',
     'expected_keywords': ['hash', 'database', 'redirect', 'unique', 'base62', 'cache'],
     'sample_answer': 'Generate a short code using base62 encoding of a unique ID. Store mapping in a database. On redirect, look up the code using Redis cache for speed. Use distributed ID generator for scale.'},
    {'category': 'hr', 'difficulty': 'easy',
     'question': 'Tell me about yourself.',
     'expected_keywords': ['experience', 'skills', 'background', 'role', 'career', 'passionate'],
     'sample_answer': 'Give a 2-minute structured pitch: background and education, key skills and technologies, 1-2 significant achievements, and why you are excited about this role.'},
    {'category': 'hr', 'difficulty': 'medium',
     'question': 'Describe a situation where you had to handle a conflict in your team.',
     'expected_keywords': ['conflict', 'communication', 'resolved', 'team', 'listen', 'outcome'],
     'sample_answer': 'Use the STAR method: Situation, Task, Action, Result. Emphasise active listening, empathy, and focusing on facts. Show you can collaborate and build consensus.'},
    {'category': 'dsa', 'difficulty': 'easy',
     'question': 'What is the time complexity of binary search?',
     'expected_keywords': ['O(log n)', 'sorted', 'mid', 'divide', 'halve', 'array'],
     'sample_answer': 'Binary search is O(log n). It works on a sorted array by repeatedly halving the search space, comparing the target with the middle element each time.'},
    {'category': 'dsa', 'difficulty': 'medium',
     'question': 'Explain the difference between a stack and a queue.',
     'expected_keywords': ['LIFO', 'FIFO', 'stack', 'queue', 'push', 'pop', 'enqueue', 'dequeue'],
     'sample_answer': 'A stack is LIFO - last in first out, like a stack of plates. A queue is FIFO - first in first out, like a ticket queue. Stacks are used in function calls; queues in job processing and BFS.'},
    {'category': 'general', 'difficulty': 'easy',
     'question': 'What is the difference between HTTP and HTTPS?',
     'expected_keywords': ['HTTP', 'HTTPS', 'SSL', 'TLS', 'encryption', 'secure', 'certificate'],
     'sample_answer': 'HTTP is unencrypted communication between browser and server. HTTPS uses SSL/TLS encryption to secure the data. HTTPS prevents man-in-the-middle attacks and is required for sensitive data.'},
    {'category': 'general', 'difficulty': 'medium',
     'question': 'What is REST API and what are its principles?',
     'expected_keywords': ['REST', 'stateless', 'HTTP', 'GET', 'POST', 'PUT', 'DELETE', 'resource'],
     'sample_answer': 'REST is an architectural style for APIs using HTTP. Key principles: stateless, client-server, uniform interface, cacheable. Uses HTTP methods GET, POST, PUT, DELETE to perform CRUD operations on resources.'},
]


class Command(BaseCommand):
    help = 'Seed interview questions'

    def handle(self, *args, **options):
        created = 0
        for q in QUESTIONS:
            obj, was_created = QuestionBank.objects.get_or_create(
                question=q['question'],
                defaults={k: v for k, v in q.items() if k != 'question'}
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created} new questions. Total: {QuestionBank.objects.count()}'
        ))
