from app.models.eisenhowers_model import EisenhowerModel



def eisenhower(data):
    importance = data['importance']
    urgency = data['urgency']
    
    eisenhowers = ''
    
    if importance == 1 and urgency == 1:
        eisenhowers = 1
    if importance == 1 and urgency == 2:
        eisenhowers = 2
    if importance == 2 and urgency == 1:
        eisenhowers = 3
    if importance == 2 and urgency == 2:
        eisenhowers = 4
        
    eisenhower_msg = EisenhowerModel.query.get(eisenhowers)
    
    return (eisenhowers, eisenhower_msg)

