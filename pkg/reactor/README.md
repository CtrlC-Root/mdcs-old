# reactor

An event based automation tool.

## Roadmap

* [ ] Implement Condition objects.
* [ ] Implement Event objects.
* [ ] Implement flow graphs connecting Event, Condition, and Action objects.
  * https://networkx.github.io/
  * http://igraph.org/python/
* [ ] Implement Linux specific script backend using seccomp kernel API.
  * http://doc.pypy.org/en/latest/sandbox.html
  * https://github.com/dw/scratch/blob/master/seccomp.py
  * https://eigenstate.org/notes/seccomp
  * https://pythonhosted.org/python-prctl/
* [ ] Implement OS X specific script backend using sandbox kernel API.
  * https://www.chromium.org/developers/design-documents/sandbox/osx-sandboxing-design

## References

Services:

* [Beanstalkd](http://kr.github.io/beanstalkd/)

Libraries:

* [Flask](http://flask.pocoo.org/docs/1.0/)
* [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/)
* [Alembic](http://alembic.zzzcomputing.com/en/latest/)
* [Marshmallow](https://marshmallow.readthedocs.io/en/2.x-line/)
* [Greenstalk](https://greenstalk.readthedocs.io/en/latest/)
