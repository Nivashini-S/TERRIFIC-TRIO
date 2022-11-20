def test(x,y):
    if((x>2 and x<100) or (y>1 and y<130)):
            return "1"
    elif((x>100 and x<250) or (y>8 and y<240)):
            return "2"
    elif((x>300 and x<350) or (y>80 and y<150)):
            return "3"
    elif((x>400 and x<550) or (y>5 and y<85)):
            return "4"    
    else:
            return "Out of Bounds"
