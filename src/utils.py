from pydantic import BaseModel


# {'uuid': 'df6b2b96-a938-48b0-83d8-75bfed059a3d',
#  'persona': 'A disciplined, sociable visionary, Jonathan balances practicality with curiosity, leaving a lasting impact on his community through his organized, competitive approach',
#  'professional_persona': 'A retired manufacturing manager, Jonathan now excels as a community developer, leveraging his organizational skills and competitive nature to drive sustainable growth in Wickliffe',
#  'sports_persona': 'An avid golfer, Jonathan plays weekly at the Wickliffe Country Club and cheers for the Cleveland Browns, maintaining his competitive spirit even in leisure',
#  'arts_persona': "A history enthusiast, Jonathan often leads tours at the Lake County Historical Society, sharing stories about local pioneers and their impact on the region's development",
#  'travel_persona': 'A seasoned, meticulous planner, Jonathan favors international destinations with rich histories, like Edinburgh and Dublin, where he can explore ancestral roots and enjoy a round of golf at prestigious courses',
#  'culinary_persona': "A fan of hearty, Midwestern comfort food, Jonathan enjoys cooking traditional family recipes, like his grandmother's beef stew, and hosting potlucks at his home",
#  'skills_and_expertise': "Jonathan's organizational skills and discipline have served him well in his career and personal life. He's proficient in project management, having led numerous successful projects in his manufacturing days. He's also skilled in budgeting and financial planning, a result of his high standards and attention to detail. His sociability has made him an effective communicator and negotiator, skills he's used extensively in his community involvement.",
#  'skills_and_expertise_list': "['project management', 'budgeting and financial planning', 'negotiation', 'community development', 'fundraising']",
#  'hobbies_and_interests': "Jonathan enjoys a mix of social and solitary activities. He's an avid golfer, playing weekly with his friends from the Wickliffe Country Club. He also enjoys woodworking in his garage, creating intricate furniture pieces that he donates to local charities. He's a member of the Lake County Historical Society, often leading tours at the local museum, and he's known for his impressive collection of vintage coins. Despite his competitive nature, he loves hosting game nights at his house, where he ensures everyone has a fair chance to win.",
#  'hobbies_and_interests_list': "['golfing', 'woodworking', 'coin collecting', 'history', 'board games and puzzles']",
#  'career_goals_and_ambitions': "After retiring from his career in manufacturing management, Jonathan has focused his ambition on community development. He's actively involved in the Wickliffe Chamber of Commerce, aiming to bring new businesses to the town. He also serves on the Lake County Planning Commission, working towards sustainable development. Despite his competitive nature, he's more interested in leaving a lasting impact on his community than personal gain.",
#  'sex': 'Male',
#  'age': 72,
#  'marital_status': 'widowed',
#  'education_level': 'high_school',
#  'bachelors_field': None,
#  'occupation': 'not_in_workforce',
#  'city': 'Wickliffe',
#  'state': 'OH',
#  'zipcode': '44092',
#  'country': 'USA'}

class Persona(BaseModel):
    persona: str
    professional_persona: str
    sports_persona: str
    arts_persona: str
    travel_persona: str
    culinary_persona: str
    skills_and_expertise: str
    skills_and_expertise_list: list[str]
    hobbies_and_interests: str
    hobbies_and_interests_list: list[str]
    career_goals_and_ambitions: str
    
    
class PersonaChatResponse(BaseModel):
    llm_response: str
    persona_response: Persona
    