#


import cv2
import numpy as np
from PIL import Image
from stockfish import Stockfish
import keyboard 

#STOCKFISH
#tune parameters to make stockfish stronger, but will make the code laggier
stockfish = Stockfish(path="C:\\Users\\neong\\Downloads\\stockfish\\stockfish\\stockfish-windows-x86-64-avx2.exe", depth=10, parameters={"Threads": 2, "Minimum Thinking Time": 0})
stockfish.update_engine_parameters({
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1, 
    "Ponder": False,
    "Hash": 16, 
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 0,
    "Slow Mover": 0,
    "UCI_Chess960": False,
    "UCI_LimitStrength": False,
    "UCI_Elo": 1350
})


#COORDINATES ----------------------------------------------------------------------------------
#defines cropping of the full image
x_start = 135
x_end = 515
y_start = 45
y_end = 435
#defines edges of grid lines
x1 = 5
y1 = 5
x2 = 375
y2 = 385
#coordinates of the bounding box for the capture color detection
xx1 = 0
yy1 = 0
xx2 = 1
yy2 = 1

#ARRAYS ----------------------------------------------------------------------------------------
#arrays for counting contours
s6=np.zeros((8,8), dtype=int)
s5=np.zeros((8,8), dtype=int)
s4=np.zeros((8,8), dtype=int)
s3=np.zeros((8,8), dtype=int)
s2=np.zeros((8,8), dtype=int)
s1=np.zeros((8,8), dtype=int)
#array to show gone pieces and new pieces on the board
pieces = np.zeros((8,8), dtype=int)
#array with current position of pieces, constantly updating
squares = np.zeros((8,8), dtype=int) 
#arrays for position change detection
new = np.zeros((8,8), dtype=int) 
old = np.zeros((8,8), dtype=int)
#arrays to map x y coords in arrays to notation
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#arrays for position change 
other_new = np.zeros((8,8), dtype=int)
other_old = np.zeros((8,8), dtype=int)
#color codes for communicating
move_color = [(0,0,255), (0,165,255), (0,255,255), (0,255,0), (255,255,0), (255,0,0), (255, 0, 200), (255, 0, 255)]
#             red         orange        yellow      green      blue-green    blue       purple        magenta

#OTHER STUFF ------------------------------------------------------------------------------------
hand = 3 #for making the position change thing only run once
waiting = 0
key = cv2.waitKey(1) & 0xFF #key pressed checker thing  
bbox_ = (0,0,0,0) #bounding box for hand det initialization
count = 0 #how many loops of the while True loop have been run, used to set new_img and result 
move = "0000" #move being fed to stockfish
turn = 0 #tracks who's turn it is
cap = cv2.VideoCapture(0) #which camera to read from
skin = [20, 20, 75] # skin tone of hand for hand detection
position = 0 #finds what color to flash
end = 0,0
hand_found = 0
bboxyn = 0
move_type = "init"
delay = 1000
light = np.zeros((500, 500, 3), dtype='uint8')

def get_limits(color):
    #finding limits of what classifies as skin tone for a hand
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c,cv2.COLOR_BGR2HSV)
    lowerLimit = hsvC[0][0][0] - 0, 180, 50
    upperLimit = hsvC[0][0][0] + 20, 200, 90
    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)
    return lowerLimit, upperLimit

def find_coords(array, target): 
    #find coordinates of gone and new pieces in arrays
    for i in range(8):
        for j in range(8): 
            if array[i][j] == target: 
                return (i, j) 
    return None

def find_not(start, end):
    global x_coord, y_coord, x2_coord, y2_coord
    #converts coordinates into chess notation useable by stockfish
    if start == None or end == None:
        print('missing coordinate', start, end)
    else:
        x_coord, y_coord = start
        start_x = letters[x_coord]
        start_y = numbers[y_coord]
        x2_coord, y2_coord = end
        end_x = letters[x2_coord]
        end_y = numbers[y2_coord]
        move = start_x + start_y + end_x + end_y
        return move

def capture_coords():
    global xx1, yy1, xx2, yy2, avgx, avgy, xoff, yoff, row_space, column_space, height, width, end
    #converts location of the captured piece bbox into coordinates in the 8x8 grid
    avgx = (xx1 + xx2)/2
    avgy = (yy1 + yy2)/2
    row_space=width/8
    column_space=height/8
    row = 0
    column = 0
    start_x1 = 5
    start_y1 = 5
    for a in range (8):
        if start_x1 + 12 < avgx < (2 + row_space) - 12:
            for b in range (8):
                if start_y1 + 12 < avgy < (16 + column_space) - 12:
                    end = column, row
                else:
                    pass
                start_y1 = start_y1 + yoff
                column_space = column_space + yoff
                column = column + 1
        else:
            pass
        start_x1 = start_x1 + xoff
        row_space = row_space + xoff
        row = row + 1
    return end

def not2int(input):
    #switches stockfish's move notation into integers
    output = 8
    if input == 'a' or input == '1':
        output = 0
    if input == 'b' or input == '2':
        output = 1
    if input == 'c' or input == '3':
        output = 2
    if input == 'd' or input == '4':
        output = 3
    if input == 'e' or input == '5':
        output = 4
    if input == 'f' or input == '6':
        output = 5
    if input == 'g' or input == '7':
        output = 6
    if input == 'h' or input == '8':
        output = 7
    return output

#start sequence
print('press w or b')
#press w to play white and b to play black

while True:
    if keyboard.is_pressed("b"):
        side = 0
        break
    elif keyboard.is_pressed("w"):
        side = 1
        break

print('starting')

#main code
while True:
    #create flashing light window
    light[0:500, 0:500] = 0,0,0
    cv2.imshow('light', light)

    #set arrays
    s7 = s6
    s6 = s5
    s5 = s4
    s4 = s3
    s3 = s2
    s2 = s1
    s1 = squares

    #read new frame
    ret, big_frame = cap.read()

    #crop frame
    frame = big_frame[y_start:y_end, x_start:x_end]
    cv2.imshow('og', big_frame)
    cv2.line(frame, (180, 195), (200, 195), (0,255,0), 2)
    cv2.line(frame, (190, 185), (190, 205), (0,255,0), 2)
    cv2.imshow('Cropped 1', frame)

    #get images for before/after capture comparasion
    comp_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #if its the initial loop set some variables
    if count == 0:
        new_img = comp_img #prep comparison images
        result = comp_img
        pieces[0:8, 0:2] = 2 #prep pieces array
        pieces[0:8, 6:8] = 2

    #hand detection
    hsvimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #convert to HSV for better tuning
    lowerLimit, upperLimit = get_limits(color=skin) #find upper/lower limit for the color of what classifies as a hand
    mask = cv2.inRange(hsvimg, lowerLimit, upperLimit) #masking over things that are in the color range
    mask_ = Image.fromarray(mask) #converting into useable format
    bbox_ = mask_.getbbox() #gets a bounding box based on mask dimensions
    if bbox_ is not None: #if there is a bbox_, get the coordinates, draw rectangle with those coords
        x1_, y1_, x2_, y2_ = bbox_
        width_ = x2_ - x1_
        height_ = y2_ - y1_
        if (width_*width_) <= 4000 or (height_*height_) <= 4000: #if its too small, kill the bbox_
            bbox_ = None
            bboxyn = 0
        else:
            frame = cv2.rectangle(frame, (x1_,y1_), (x2_,y2_), (0,255,255), 5) #draws bbox_
            bboxyn = 1
    cv2.imshow('Hand Det 2',frame)

    #blank image for mask
    blank = np.zeros(frame.shape[:2], dtype='uint8')

    #masking image so its only the board
    rectangle = cv2.rectangle(blank, (x1,y1), (x2,y2), 255, -1) #x1 and the other coords are predetermined
    masked = cv2.bitwise_and(frame,frame,mask=rectangle) #masking
    cv2.imshow('Masked 3', masked) 

    #edge detection
    grayimg = cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY) #makes image gray
    canny = cv2.Canny(grayimg, 70, 70, 3, L2gradient=True) #uses canny to detect edges, can tune 2nd and 3rd parameters, lower value = more edges
    ret, thresh = cv2.threshold(grayimg, 125, 255, cv2.THRESH_BINARY) #creates contour locations
    contours, hierarchies = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #more contour location finding
    cv2.drawContours(masked, contours, -1, (0,0,255), 1) #draws contours in red with thickness 1
    cv2.imshow('Contours+Color 4', masked)

    #draws grid lines
    width = int(x2-x1)
    height = int(y2-y1)
    n = 8
    for repeat_count in range(9):
        change_x = int(x1+width*n/8)
        change_y = int(y1+height*n/8)
        cv2.line(masked, (change_x,y1), (change_x,y2), (255,255,0), 2) #vert small
        cv2.line(masked, (x1,change_y), (x2,change_y), (255,255,0), 2) #hori small
        n=n-1

    row = 0
    column = 0
    row_space = width/8
    column_space = height/8
    og_x1 = x1
    og_y1 = y1
    squares = np.zeros((8,8), dtype=int)

    #piece finder
    for cnt in contours :
        approx = cv2.approxPolyDP(cnt, 1 * cv2.arcLength(cnt, True), True)
        n = approx.ravel() 
        i = 0
        for j in n :
            if(i % 2 == 0):
                x = n[i]
                y = n[i + 1]
                string = str(x) + " " + str(y) 
                #setting variables
                xoff = width/8 
                yoff = height/8
                row_space=width/8
                column_space=height/8
                row = 0
                column = 0
                start_x1 = og_x1
                start_y1 = og_y1
                param = 12
                for a in range (8):
                    if start_x1 + param < x < (x1 + row_space) - param: #checks if contour is in a certain row
                        for b in range (8):
                            if start_y1 + param < y < (y1 + column_space) - param: #checks if contour is in a certain column in the row
                                squares[column, row] = squares[column, row] + 1 #if yes then set its location in the array to 1
                                cv2.putText(masked, 'x', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 255)) #draw an x on the screen for contours that are pieces
                            else:
                                pass
                            start_y1 = start_y1 + yoff
                            column_space = column_space + yoff
                            column = column + 1
                    else:
                        pass
                    start_x1 = start_x1 + xoff
                    row_space = row_space + xoff
                    row = row + 1
            i = i + 1
    resize = cv2.resize(masked, (860,805), interpolation=cv2.INTER_LINEAR) #size it up
    cv2.imshow('Contour Locations 5', resize)

    #piece location verifier, position change detector, move played finder, send info to claw
    if hand == 0: #if a hand just left the frame, and 30 loops have been waited
        old_img = new_img #capture comparison images
        new_img = comp_img
        old = new #old/new arrays (contour count)
        new = np.zeros((8,8), dtype=int) 
        other_old = other_new #old/new arrays (y/n)
        other_new = np.zeros((8,8), dtype=int)
        pieces = np.zeros((8,8), dtype=int) #gone/new pieces
        subtract = np.zeros((8,8), dtype=int) #old - new (contour count)
        bin_subtract = np.zeros((8,8), dtype=int) #old - new (y/n)
        hand = 2 #sets it to 2 so this part of the code only runs once 
        row_ = 0 #variable resetting
        column_ = 0
        gone_pieces = 0
        new_pieces = 0
        start_coords = (0,0)
        end_coords = (0,0)
        for q in range (8): #checks all rows
            column_ = 0
            for w in range (8): #checks all columns
                avgs = s1[column_, row_] + s2[column_, row_] + s3[column_, row_] + s4[column_, row_] + s5[column_, row_] + s6[column_, row_] + s7[column_, row_]
                if (avgs) >= 6: #checks if the contour is there for most of the time
                    other_new[column_, row_] = 1 #almost certainly a piece there, set to 1
                    new[column_,row_] = avgs/7 #almost certainly a piece there, set to whatever the average is
                else:
                    other_new[column_,row_] = 0 #probably no piece, set to 0
                    new[column_,row_] = 0 #probably no piece, set to 0
                column_ = column_ + 1
            row_ = row_ + 1
        row_ = 0 
        column_ = 0
        for r in range (8): #checking all rows
            column_ = 0
            for t in range (8): #checking all columns
                min_cnt = 1 #minimum amount of contours change to qualify as a gone/new piece
                subtract[column_,row_] = old[column_,row_] - new[column_,row_] #subtract the old from the new (contour count)
                bin_subtract[column_,row_] = other_old[column_,row_] - other_new[column_,row_] #subtract the old from the new (y/n)
                if subtract[column_,row_] >= min_cnt and bin_subtract[column_,row_] == 1: #if a piece disappeared, set some variables
                    gone_pieces = gone_pieces + 1
                    pieces[column_, row_] = 1
                elif subtract[column_,row_] <= (-1 * min_cnt) and bin_subtract[column_,row_] == -1: #if a piece spawned in, set some variables
                    new_pieces = new_pieces + 1
                    pieces[column_, row_] = 2
                else: #no change
                    pass
                column_ = column_ + 1
            row_ = row_ + 1
        if gone_pieces == 1 and new_pieces == 1:
            move_type = "normal"
        elif gone_pieces == 1 and new_pieces == 0:
            move_type = "capture"
        elif gone_pieces == 2 and new_pieces == 2:
            move_type = "castle"
        elif new_pieces == 32:
            pass
        else:
            #trying to filter out the squares which registered a gone/new piece until there is a valid amount by ignoring the squares that have the least confidence
            min_cnt2 = 1
            column_ = 0
            row_ = 0
            go = 1
            while go == 1:
                gone_pieces = 0
                new_pieces = 0
                row_ = 0
                for v in range (8): #checks all rows
                    column_ = 0
                    for b in range (8): #checks all columns
                        if subtract[column_,row_] == 0:
                            pass
                            #print('nothing')
                        else:
                            if abs(subtract[column_,row_]) <= min_cnt2:
                                bin_subtract[column_,row_] = 0
                                #print('found')
                        column_ = column_ + 1
                    row_ = row_ + 1
                row_ = 0
                pieces2 = pieces
                for r in range (8): #checking all rows
                    column_ = 0
                    for t in range (8): #checking all columns
                        if bin_subtract[column_,row_] == 1: #if a piece disappeared, set some variables
                            gone_pieces = gone_pieces + 1
                            pieces2[column_, row_] = 1
                        elif bin_subtract[column_,row_] == -1: #if a piece spawned in, set some variables
                            new_pieces = new_pieces + 1
                            pieces2[column_, row_] = 2
                        else: #no change
                            pieces2[column_,row_] = 0
                        column_ = column_ + 1
                    row_ = row_ + 1
                #recheck after filtering if the new sets of gone and new piece satisfy any move types
                if gone_pieces == 1 and new_pieces == 1:
                    move_type = "normal"
                    pieces = pieces2
                    go = 0
                elif gone_pieces == 1 and new_pieces == 0:
                    move_type = "capture"
                    pieces = pieces2
                    go = 0
                elif gone_pieces == 2 and new_pieces == 2:
                    move_type = "castle"
                    pieces = pieces2
                    go = 0
                else:
                    pass
                if min_cnt2 == 20: #after 20 loops it gives up and ignores the move
                    go = 0
                min_cnt2 = min_cnt2 + 1
        #checks what kind of move got played
        if move_type == "normal": #standard move
            start_coords = find_coords(pieces, 1) #finding coords
            end_coords = find_coords(pieces, 2) 
            move = find_not(start_coords, end_coords) #convert to notation
        elif move_type == "capture": #capture has been made
            old_img_2 = (old_img / 2) + 128 #adjust color space to accomodate negatives
            new_img_2 = new_img / 2
            result = cv2.subtract(old_img_2, new_img_2) #subtract images to find differences
            result_uint8 = result.astype(np.uint8)
            if side % 2 == 1: #white to move, find black spots
                lowerLimit2 = 0
                upperLimit2 = 50
            else: #black to move, find white spots
                lowerLimit2 = 205
                upperLimit2 = 255
            mask2 = cv2.inRange(result_uint8, lowerLimit2, upperLimit2) #color detection system
            mask_2 = Image.fromarray(mask2) #same as before
            bbox2 = mask_2.getbbox()
            if bbox2 is not None:
                xx1, yy1, xx2, yy2 = bbox2
            result_uint8 = cv2.rectangle(result_uint8, (xx1,yy1), (xx2,yy2), (0,255,0), 5) #draw bbox over color-swapped area (where capture was) 
            start_coords = find_coords(pieces, 1) #find coords
            end_coords = capture_coords() #convert bbox location to coordinates useable by find_not()
            move = find_not(start_coords, end_coords) #convert to notation
        elif move_type == "castle": #castle has been played, use what square a piece (rook) disappeared from to determine which castle was played
            if pieces[0,0] == 1: #white long castle
                move = "e1c1"
            elif pieces[7,0] == 1: #white short castle
                move = "e1g1"
            elif pieces[0,7] == 1: #black long castle
                move = "e8c8"
            elif pieces[7,7] == 1: #black short castle
                move = "e8g8"
        else:
            pass
        #have stockfish update the position 
        stockfish.set_fen_position(stockfish.get_fen_position())
        legal_moves = [m['Move'] for m in stockfish.get_top_moves(40)]  
        if move in legal_moves:
            stockfish.make_moves_from_current_position([move])
            turn = turn + 1
        else:
            print("Illegal move!")
        if turn % 2 == side: #check if its stockfish's turn
            turn = turn + 1
            bot_move = stockfish.get_best_move()
            light[0:500, 0:500] = 0,255,0 #start looking at colors (green)
            cv2.imshow('light', light)
            cv2.waitKey(delay) #waits a bit
            stockfish.set_fen_position(stockfish.get_fen_position())
            start1, start2, end1, end2 = bot_move
            ending = end1 + end2
            if bot_move == "e1c1" or bot_move == "e1g1" or bot_move == "e8c8" or bot_move == "e8g8": #determines if the move is a castle or not
                light[0:500, 0:500] = 73, 83, 255 #red-orange symbolizes castling
                cv2.imshow('light', light)
                cv2.waitKey(delay)
                if bot_move == "e1c1": #white long
                    light[0:500, 0:500] = 255,0,0 #blue = white long caste
                    cv2.imshow('light', light)    
                    cv2.waitKey(delay)         
                elif bot_move == "e1g1": #white short
                    light[0:500, 0:500] = 0,255,0 #green = white short castle
                    cv2.imshow('light', light)
                    cv2.waitKey(delay)
                elif bot_move == "e8c8": #black long
                    light[0:500, 0:500] = 0, 0, 255 #red = black long castle
                    cv2.imshow('light', light)
                    cv2.waitKey(delay)
                else: #black short
                    light[0:500, 0:500] = 0,255,255 #yellow = black short castle
                    cv2.imshow('light', light)  
                    cv2.waitKey(delay)                                                      
            else: 
                if stockfish.get_what_is_on_square(ending) is not None:
                    light[0:500, 0:500] = 50, 205, 154 #yellow-green symbolizes direct (normal) capture
                    print('move is a capturee')
                    cv2.imshow('light', light)
                    cv2.waitKey(delay)
                else:
                    light[0:500, 0:500] = 255, 0, 255 #magenta symbolizes normal move
                    cv2.imshow('light', light)
                    cv2.waitKey(delay)
                #converting the bot move to integers
                bot_x, bot_y, bot_x2, bot_y2 = bot_move
                bot_x = not2int(bot_x)
                bot_y = not2int(bot_y)
                bot_x2 = not2int(bot_x2)
                bot_y2 = not2int(bot_y2)
                move_array = np.array([bot_x, bot_y, bot_x2, bot_y2])
                number = 0
                position = 8
                for n in range (4): #flashes 4 colors to show each step of notation
                    position = move_array[number] #goes through each piece integers (which represents notation)
                    color_code = move_color[position] #takes the integers and assigns the correct color to represent it
                    light[0:500, 0:500] = color_code
                    cv2.imshow('light', light)
                    cv2.waitKey(delay)
                    number = number + 1
            light[0:500, 0:500] = 0,0,255 #red tells brain to stop looking at the color
            cv2.imshow('light', light)
            cv2.waitKey(delay)
            light[0:500, 0:500] = 0,0,0 #goes back to black
            cv2.imshow('light', light)
            stockfish.make_moves_from_current_position([bot_move]) #makes the move

    #system to only run the above function when desired and only once until the next time it is needed comes
    if hand_found == 1 or bboxyn == 1: #if hand bbox (hand found), hand = 1
        hand = 1
    elif hand == 2: #if its 2 ignore
        pass
    else: #if its anything else...
        if not hand == 2 and waiting == 0: #if hand isn't 2 and waiting is 0 (hand just got set to 0)
            hand = 3 
            waiting = 1 #set waiting to 1 and reset loops (start counting loops)
            loops = 0
        if loops == 30: #when 30 loops have been run through after the initial detection of a hand, hand = 0 and waiting = 0
            waiting = 0
            hand = 0
        elif waiting == 1: #when counting, add a loop
            if bboxyn == 1:
                waiting = 0
                loops = 0
            else:
                loops = loops + 1
        pass

    #to ensure new_img and result are only set once to frame 
    count = count + 1

    #stopping the code
    key = cv2.waitKey(1) & 0xFF   
    if key == ord('q'): 
        break

#stop program
cap.release()
cv2.destroyAllWindows
