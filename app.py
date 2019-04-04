from blog import app
import blog.movieserver as movieserver
from multiprocessing import Process

if __name__ == '__main__':
    p0 = Process(target = movieserver.M)
    p0.start()
    p1 = Process(app.run(debug=True))
    p1.start()
