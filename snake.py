import pygame
import time
import random
import numpy as np
import math

window_x = 720
window_y = 480
def taxa(n):
    return 1 - (.5)**(1/n)

def geracao_pop_inicail(n:int):
    ante = np.random.choice(['0','1','#'],(n,12))
    cons = np.random.randint(0,2,(n,2))
    energia = np.full(n,100.0)
    return ante,cons,energia

def dist(pos1,pos2):
    x = (pos1[0] - pos2[0])**2
    y = (pos1[1] - pos2[1])**2
    return (x+y)**.5

def radar(pos,f_pos,s_body):
    if pos[0] == f_pos[0] and pos[1] == f_pos[1]:
        return '11'
    elif pos[0] < 0 or pos[0] > window_x-10:
        return '01'
    elif pos[1] < 0 or pos[1] > window_y-10:
        return '01'
    else:
        for block in s_body[1:]:
            if pos[0] == block[0] and pos[1] == block[1]:
                return '10'
    return '00'

def geracao_msg(dir,f_pos,s_pos,s_body):
    msg = ''
    xs,ys= s_pos
    
    if dir == 'RIGHT':
        msg+='01'
        p1 = [xs,ys-10]
        p2 = [xs+10,ys]
        p3 = [xs,ys+10]
    
    elif dir == 'LEFT':
        msg+='10'
        p1 = [xs,ys+10]
        p2 = [xs-10,ys]
        p3 = [xs,ys-10]

    elif dir == 'DOWN':
        msg+='00'
        p1 = [xs+10,ys]
        p2 = [xs,ys+10]
        p3 = [xs-10,ys]

    elif dir == 'UP':
        msg+='11'
        p1 = [xs-10,ys]
        p2 = [xs,ys-10]
        p3 = [xs+10,ys]

    msg+=radar(p1,f_pos,s_body)
    msg+=radar(p2,f_pos,s_body)
    msg+=radar(p3,f_pos,s_body)

    if xs > f_pos[0]:
        msg+='10'
    elif xs< f_pos[0]:
        msg+='01'
    else:
        msg+='11'

    if ys > f_pos[1]:
        msg+='10'
    elif ys< f_pos[1]:
        msg+='01'
    else:
        msg+='11'

    return  np.fromiter(msg,dtype="S1").astype(str) 

def similaridade(rule,msg):
    return np.count_nonzero(rule=='#') + np.count_nonzero(msg==rule)

def especificidade(rule):
    return np.count_nonzero(rule=='#')/len(rule)

def selecionar_msg(pop,msg):
    _similaridade = np.apply_along_axis(similaridade,1,pop,msg=msg)
    maxi = _similaridade.max()
    return np.where(_similaridade==maxi)[0]

def bit(energia,rules,k0,k1,k2,p):
    spec = np.apply_along_axis(especificidade,1,rules)
    return k0*(k1+k2*(spec**p))*energia

def ebit(energia,rules,sigma,bit_tax):

    _bit = bit(energia,rules,.01,.5,.01,1)
    noise = np.random.normal(size=len(rules))
    return abs(_bit - sigma*noise),_bit,_bit*bit_tax

def leilao(indi,rules,energia):
    while True:
        _ebit,_bit,tax = ebit(energia[indi],rules[indi],.001,.01)
        winner = indi[_ebit.argmax()]
        if _ebit.min()>0:
            break
        break
    return _bit[_ebit.argmax()],winner,tax

def recompensa(pos_s,pos_f,body_s,_dist):
    if pos_s[0] == pos_f[0] and pos_s[1] == pos_f[1]:
        return 10
    elif pos_s[0]<0 or pos_s[0]>window_x-10:
        return -5
    elif pos_s[1]<0 or pos_s[1] > window_y-10:
        return -5
    elif pos_s in body_s[1:]:
        return -10
    elif dist(pos_s,pos_f)< _dist:
        return 1
    else:
        return -.5
    return 0
    

def selecao(energia,pp):
    aux = np.argsort(energia)
    pp=int(len(energia)*pp)
    return aux[-pp:],aux[:pp]



def reproducao(ant,cons,energia):
    ant_filho,cons_filho,energia_filho = [],[],[]
    pai1 = range(0,len(ant)//2,)
    pai2 = range(len(ant)//2,len(ant))
    np.random.uniform()
    for p1,p2 in zip(pai1,pai2[::-1]):
        ant_c = np.random.uniform(-1,1,12)
        neg = len(np.where(ant_c<0))
        pos = 12 - neg
        ant_f1 = np.where(ant_c<0,ant[p1],ant[p2])
        ant_f2 = np.where(ant_c>=0,ant[p1],ant[p2])
        if neg>6:
            cons_f1=cons[p1].copy()
            cons_f2 = cons[p2].copy()
        else:
            cons_f1=cons[p2].copy()
            cons_f2 = cons[p2].copy()

        e1 = (neg*energia[p1]+pos*energia[p2])/12
        e2 = (pos*energia[p1]+neg*energia[p2])/12

    

        # pc = random.randint(0,len(ant))
        # ant_f1 = np.concatenate((ant[p1][:pc],ant[p2][pc:]))
        # ant_f2 = np.concatenate((ant[p2][:pc],ant[p1][pc:]))
        # cons_f1 = cons[p2] 
        # cons_f2 = cons[p1]
        # ener_f = (energia[p1]+energia[p2])/2
        ant_filho.append(ant_f1)
        ant_filho.append(ant_f2)
        cons_filho.append(cons_f1)
        cons_filho.append(cons_f2)
        energia_filho.append(e1)
        energia_filho.append(e2)
    return np.array(ant_filho),np.array(cons_filho),np.array(energia_filho)

def mutacao(ant,cons):
    pm = random.randint(0,len(ant)+len(cons)-1)
    if pm >=len(ant):
        pm-=len(ant)
        if cons[pm] == '0':
            cons[pm] = '1'
        else:
            cons[pm] = '0'
    else:
        prob = random.uniform(0,1)
        if ant[pm]=='#':
            if prob <.5:
                ant[pm] = '0'
            else:
                ant[pm] = '1'
        elif ant[pm]=='0':
            if prob <.5:
                ant[pm] = '#'
            else:
                ant[pm] = '1'
        else:
            if prob <.5:
                ant[pm] = '#'
            else:
                ant[pm] = '0'
    return ant,cons

def snake():
    count = 0
    g = 1
    snake_speed = 300
    _taxa = taxa(250)
    # Window size
    window_x = 720
    window_y = 480
    
    # defining colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    
    # Initialising pygame
    pygame.init()
    

    # Initialise game window
    pygame.display.set_caption('EvoSnake')
    game_window = pygame.display.set_mode((window_x, window_y))


    ante,cons,energia = geracao_pop_inicail(5000)
    
    # FPS (frames per second) controller
    fps = pygame.time.Clock()
    while True:
        # defining snake default position
        snake_position = [100, 50]
        
        # defining first 4 blocks of snake body
        snake_body = [[100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                    ]
        # fruit position
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                        random.randrange(1, (window_y//10)) * 10]
        # fruit_position = [150,50]
        fruit_spawn = True
        
        # setting default snake direction towards
        # right
        direction = 'RIGHT'
        change_to = direction
        
        # initial score
        score = 0
        
        # displaying Score function
        def show_score(choice, color, font, size):
        
            # creating font object score_font
            score_font = pygame.font.SysFont(font, size)
            score_font1 = pygame.font.SysFont(font, size)
            # create the display surface object
            # score_surface
            score_surface = score_font.render('Score : ' + str(energia[winner])+' '+str(energia.min())+' '+ str(g), True, color)
            score_surface1 = score_font1.render('Score : ' + str(dist_s_f), True, color)
            # create a rectangular object for the text
            # surface object
            score_rect = score_surface.get_rect()
            score_rect1 = score_surface1.get_rect()
            # displaying text
            
            game_window.blit(score_surface, score_rect)
            
        
        # game over function
        def game_over():
        
            # creating font object my_font
            my_font = pygame.font.SysFont('times new roman', 50)
            
            # creating a text surface on which text
            # will be drawn
            game_over_surface = my_font.render(
                'Your Score is : ' + str(score), True, red)
            
            # create a rectangular object for the text
            # surface object
            game_over_rect = game_over_surface.get_rect()
            
            # setting position of the text
            game_over_rect.midtop = (window_x/2, window_y/4)
            
            # blit will draw the text on screen
            game_window.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            
            # after 2 seconds we will quit the program
            time.sleep(2)
            
            # deactivating pygame library
            pygame.quit()
            
            # quit the program
            quit()
        
        
        # Main Function
        while True:
            
            dist_s_f = dist(snake_position,fruit_position)
            #geracao de msg
            msg = geracao_msg(dir=direction,f_pos=fruit_position,s_pos=snake_position,s_body=snake_body)
            #tratamento de msg
            selecionados = selecionar_msg(ante,msg)
            while True:
                if np.sum(energia<0):
                    pass
                selecionados = selecionados[energia[selecionados]>0]
                lance,winner,tax = leilao(selecionados,ante,energia)
                if energia[winner]<0:
                    pass
                energia[winner]-=lance
                energia[selecionados]-=tax
                if energia[winner]<0:
                    pass
                #leilao
                # handling key events

                acao = ''.join(str(i) for i in cons[winner])
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_UP:
                    #         change_to = 'UP'
                    #     if event.key == pygame.K_DOWN:
                    #         change_to = 'DOWN'
                    #     if event.key == pygame.K_LEFT:
                    #         change_to = 'LEFT'
                    #     if event.key == pygame.K_RIGHT:
                    #         change_to = 'RIGHT'
                        if event.key == pygame.K_SPACE:
                            pygame.quit()
                            quit()
                if acao == '00':
                    change_to = 'DOWN'
                elif acao == '01':
                    change_to = 'RIGHT'
                elif acao == '10':
                    change_to = 'LEFT'
                elif acao == '11':  
                    change_to='UP'

                
                # If two keys pressed simultaneously
                # we don't want snake to move into two
                # directions simultaneously
                if change_to == 'UP' and direction != 'DOWN':
                    direction = 'UP'
                    break
                if change_to == 'DOWN' and direction != 'UP':
                    direction = 'DOWN'
                    break
                if change_to == 'LEFT' and direction != 'RIGHT':
                    direction = 'LEFT'
                    break
                if change_to == 'RIGHT' and direction != 'LEFT':
                    direction = 'RIGHT'
                    break
                
                show_score(1, white, 'times new roman', 20)
                energia[winner]-=10

            #execução
            #retroalimentoção
            # Moving the snake
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10

            energia[winner]+=recompensa(snake_position,fruit_position,snake_body,dist_s_f)
            # Snake body growing mechanism
            # if fruits and snakes collide then scores
            # will be incremented by 10
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 10
                fruit_spawn = False
            else:
                snake_body.pop()
                
            if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                random.randrange(1, (window_y//10)) * 10]
                
            fruit_spawn = True
            game_window.fill(black)
            
            for pos in snake_body:
                pygame.draw.rect(game_window, green,
                                pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(game_window, white, pygame.Rect(
                fruit_position[0], fruit_position[1], 10, 10))
        
            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x-10:
                # game_over()
                
                break
            if snake_position[1] < 0 or snake_position[1] > window_y-10:
                # game_over()
                
                break
            
            flag_touch = False
            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    # game_over()
                    flag_touch = True
                    break
            if flag_touch : break
        
            # displaying score continuously
            show_score(1, white, 'times new roman', 20)
        
            # Refresh game screen
            pygame.display.update()
        
            # Frame Per Second /Refresh Rate
            fps.tick(snake_speed)
            energia=(1-_taxa)*energia
            
            # energia = np.where(energia<0,0,energia)
            count+=1

            if count==250:
                count = 0
                g+=1
                
                melhores,piores = selecao(energia,.2)
                ant_f,cons_f,energia_f = reproducao(ante[melhores],cons[melhores],energia[melhores])
                ante[piores] = ant_f
                cons[piores] = cons_f
                energia[piores] = energia_f
                mut = random.sample(range(100),int(len(ante)*.01))
                for i in mut:
                    ante[i],cons[i] = mutacao(ante[i],cons[i])

                


snake()