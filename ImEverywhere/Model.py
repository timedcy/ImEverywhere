#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from py2neo.ogm import GraphObject, Property, Related, RelatedTo, RelatedFrom


class Activity(GraphObject):
    __primarykey__ = "name"

    name = Property()
    cname = Property()
    tagline = Property()
    released = Property()
    purpose = Property()

    actors = RelatedFrom("Person", "ACTED_IN")
    knowledges = RelatedFrom("Knowledge", "USED_IN")
    stories = RelatedFrom("Story", "SHARED_IN")
    media = RelatedFrom("Media", "NEEDED_IN")
    link_with = Related("Activity", "LINK_WITH")
    comment = RelatedTo("Comment", "ACTIVITY_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("actors", "Person"), ("knowledges", "Knowledge"), ("stories", "Story"), ("media", "Media"), ("link_with", "Activity"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.name < other.name


class Person(GraphObject):
    __primarykey__ = "name"

    name = Property()
    cname = Property()
    born = Property()
    gender = Property()
    hometown = Property()
    phone = Property()
    interest = Property()
    goodat = Property()
    vegan_time = Property()
    guider = Property()
    learn_time = Property()
    tutor = Property()

    acted_in = RelatedTo("Activity", "ACTED_IN")
    knows = Related("Person", "KNOWS")
    comment = RelatedTo("Comment", "PERSON_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("acted_in", "Activity"), ("knows", "Person"), ("comment", "Comment")]
	
    def __lt__(self, other):
        return self.name < other.name
		
		
class Summary(GraphObject):
    __primarykey__ = "name"
	
    date = Property()
    name = Property()
    cname = Property()
    text = Property()

    link_with = Related("Summary", "LINK_WITH")
    comment = RelatedTo("Comment", "SUMMARY_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("link_with", "Summary"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.name < other.name

		
class Knowledge(GraphObject):
    __primarykey__ = "name"
    
    name = Property()
    cname = Property()
    definition = Property()
    content = Property()
    tag = Property()

    used_in = RelatedTo("Activity", "USED_IN")   
    link_with = Related("Knowledge", "LINK_WITH")
    comment = RelatedTo("Comment", "KNOWLEDGE_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("used_in", "Activity"), ("link_with", "Knowledge"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.name < other.name

class Classic(Knowledge):
    __primarykey__ = "name"
    
    name = Property()
    cname = Property()
    classification = Property()
    content = Property()
    tag = Property()
   
    link_with = Related("Classic", "LINK_WITH")
    point_in = RelatedFrom("Story", "POINT")
    comment = RelatedTo("Comment", "CLASSIC_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("link_with", "Knowledge"), ("point_in", "Story"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.name < other.name
		
class Story(GraphObject):
    __primarykey__ = "name"

    name = Property()
    cname = Property()
    classification = Property()
    author = Property()
    content = Property()
    purpose = Property()

    shared_in = RelatedTo("Activity", "SHARED_IN")
    points = RelatedTo("Classic", "POINT")
    link_with = Related("Story", "LINK_WITH")
    comment = RelatedTo("Comment", "STORY_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("shared_in", "Activity"), ("points", "Classic"), ("link_with", "Story"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.name < other.name


class Media(GraphObject):
    __primarykey__ = "name"

    name = Property()
    cname = Property()
    classification = Property()
    author = Property()
    released = Property()
    content = Property()
    purpose = Property()

    needed_in = RelatedTo("Activity", "NEEDED_IN")
    comment = RelatedTo("Comment", "MEDIA_COMMENT")
	# All 'RelatedTo' relationships of itself
    related = [("needed_in", "Activity"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.name < other.name

		
class Comment(GraphObject):
    __primarykey__ = "name"
	
    date = Property()
    name = Property()
    cname = Property()
    rate = Property()
    text = Property()

    activity = RelatedFrom("Activity", "ACTIVITY_COMMENT")
    person = RelatedFrom("Person", "PERSON_COMMENT")
    summary = RelatedFrom("Summary", "SUMMARY_COMMENT")
    knowledge = RelatedFrom("Knowledge", "KNOWLEDGE_COMMENT")
    story = RelatedFrom("Story", "STORY_COMMENT")
    media = RelatedFrom("Media", "MEDIA_COMMENT")
    classic = RelatedFrom("Classic", "CLASSIC_COMMENT")
    comment = Related("Comment", "LINK_WITH")
	# All 'RelatedTo' relationships of itself
    related = [("activity", "Activity"), ("person", "Person"), ("summary", "Summary"), ("knowledge", "Knowledge"), ("story", "Story"), ("media", "Media"), ("classic", "Classic"), ("comment", "Comment")]

    def __lt__(self, other):
        return self.date < other.date
		