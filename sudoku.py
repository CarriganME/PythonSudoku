import sys
import pygame
from settings import Settings

BLACK = [0, 0, 0]
LIGHTGRAY = [100, 100, 100]
BLUE = [55, 170, 200]
LIGHTBLUE = [100,240, 240]
RED = [255, 0, 0]

class Sudoku:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.xBox = [0,100,200,300,400,500,600,700,800,900]
        self.yBox = [0,100,200,300,400,500,600,700,800,900]

        #Run in windowed more
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        #Run in full screen
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Sudoku")


    def run_game(self):
        """Start the main loop for the game"""
        running = True
        mouseClicked = False
        
        while running:
            
            mouseClicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos

                #Mouse click commands
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
                
                elif event.type == pygame.KEYDOWN:
                    self.settings.input = pygame.key.name(event.key)

            if mouseClicked == True:
                self.settings.mouse_x = mousex
                self.settings.mouse_y = mousey

            #Watch for keyboard and mouse events
        #   self._check_events()

            #Redraw the screen during each pass through of the loop
            self._update_screen()
        pygame.quit()

    def _update_screen(self):
        """Update images on the screen, and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        
        self._find_box()
        if self.settings.current_x_coord < self.settings.screen_width and self.settings.current_y_coord < self.settings.screen_height:
            self._highlight_current_box()
        self._draw_grid()
        self._save_num()
        self._fill_num_grid()
        self._check_collision()
        self._check_completion()
        self._timer()
        print(self.settings.hasError)
        

        #Make the most recently drawn screen visible
        pygame.display.flip()

    def _draw_grid(self):
        """Draw grid on screen"""
        #Draw minor lines
        for x in range(0, self.settings.screen_width - 300, self.settings.cell_size):
            pygame.draw.line(self.screen, LIGHTGRAY, (x,0), (x,self.settings.screen_height))

        for y in range(0, self.settings.screen_height, self.settings.cell_size):
            pygame.draw.line(self.screen, LIGHTGRAY, (0,y), (self.settings.screen_width - 300, y))

        #Draw major lines
        for x in range(0, self.settings.screen_width - 200, self.settings.square_size):
            pygame.draw.line(self.screen, BLACK, (x,0), (x,self.settings.screen_height))
            
        for y in range(0, self.settings.screen_height - 100, self.settings.square_size):
            pygame.draw.line(self.screen, BLACK, (0,y), (self.settings.screen_width - 300, y))

    def _highlight_current_box(self):
        """Highlight the currently selected box"""
        if self.settings.mouse_x <= self.settings.screen_width - 300:
            #Highlight row selected box appears in
            pygame.draw.rect(self.screen, LIGHTBLUE, (0, self.settings.current_y_coord, self.settings.screen_width - 300, self.settings.cell_size), 0)

            #Highlight cloumn selected box appears in
            pygame.draw.rect(self.screen, LIGHTBLUE, (self.settings.current_x_coord, 0, self.settings.cell_size, self.settings.screen_width), 0)

            #Highlight selected box
            pygame.draw.rect(self.screen, BLUE, (self.settings.current_x_coord, self.settings.current_y_coord, self.settings.cell_size, self.settings.cell_size), 0)

    def _find_box(self):
        self.settings.current_x_coord = self.settings.mouse_x
        self.settings.current_y_coord = self.settings.mouse_y

        for x in range(1,10):
            if self.xBox[x - 1] < self.settings.mouse_x < self.xBox[x]:
                self.settings.current_x_coord = self.xBox[x-1]
            if self.xBox[x - 1] < self.settings.mouse_y < self.xBox[x]:
                self.settings.current_y_coord = self.yBox[x-1]
        
        self.settings.selected_box_x = self.settings.current_x_coord // 100
        self.settings.selected_box_y = self.settings.current_y_coord // 100

    def _timer(self):     
            if self.settings.win == False:
                # Calculate total seconds
                total_seconds = self.settings.frame_count // self.settings.frame_rate
 
                # Divide by 60 to get total minutes
                minutes = total_seconds // 60
 
                # Use modulus (remainder) to get seconds
                seconds = total_seconds % 60
 
                # Use python string formatting to format in leading zeros
                output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
 
                # Blit to the screen
                text = self.settings.clockFont.render(output_string, 1, BLACK)
            
                self.screen.blit(text, [950, 50])


                self.settings.frame_count += 1
 
                # Limit frames per second
                self.settings.clock.tick(self.settings.frame_rate)
            

    def _fill_num_grid(self):
        for x in range (0, 9):
            for y in range(0,9):
                if self.settings.grid[x][y] != '':
                    text = self.settings.font.render(self.settings.grid[x][y], 1, BLACK)
                    self.screen.blit(text, (x*100 + 30, y*100 + 20))

    def _save_num(self):
        if len(self.settings.input) == 1: #and string != backspace:
            if self.settings.input != '' and 49 <= ord(self.settings.input) <= 57:
                self.settings.grid[self.settings.selected_box_x][self.settings.selected_box_y] = self.settings.input
                self.settings.input = ''
        
    def _check_completion(self):
        count = 0
        for i in range (0,9):
            for j in range(0,9):
                if self.settings.grid[i][j] != '':
                    count = count + 1
                if count == 81 and self.settings.hasError == False:
                    self.settings.win == True
        print(count)

    def _check_collision(self):
        self.settings.hasError = False
        for i in range(0,9):
            for x in range(0,9):
                for y in range(x+1,9):
                    #Vertical colission
                    if self.settings.grid[i][x] != '' and self.settings.grid[i][y] != '':
                        self._color_error(i, x, y)
                    
                    #Horizontal colission
                    if self.settings.grid[x][i] != '' and self.settings.grid[y][i] != '':
                        self._color_error(i, x, y)

        #In box collision   

        #Top Left Box
        for i in range(0,9,3):
            for j in range(0,9,3):
                if self.settings.grid[i][j] != '':
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j+1]:
                        self._color_error_box(i, j, i+1, j+1)
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j+2]:
                        self._color_error_box(i, j, i+1, j+2)
                    if self.settings.grid[i][j] == self.settings.grid[i+2][j+1]:
                        self._color_error_box(i, j, i+2, j+1)
                    if self.settings.grid[i][j] == self.settings.grid[i+2][j+2]:
                        self._color_error_box(i, j, i+2, j+2)

        #Middle Left Box
        for i in range(0,9,3):
            for j in range(1,9,3):
                if self.settings.grid[i][j] != '':
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j-1]:
                        self._color_error_box(i, j, i+1, j-1)
                    if self.settings.grid[i][j] == self.settings.grid[i+2][j-1]:
                        self._color_error_box(i, j, i+2, j-1)
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j+1]:
                        self._color_error_box(i, j, i+1, j+1)
                    if self.settings.grid[i][j] == self.settings.grid[i+2][j+1]:
                        self._color_error_box(i, j, i+2, j+1)

        #Bottom Left Box
        for i in range(0,9,3):
            for j in range(2,9,3):
                if self.settings.grid[i][j] != '':
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j-1]:
                        self._color_error_box(i, j, i+1, j-1)
                    if self.settings.grid[i][j] == self.settings.grid[i+2][j-1]:
                        self._color_error_box(i, j, i+2, j-1)
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j-2]:
                        self._color_error_box(i, j, i+1, j-2)
                    if self.settings.grid[i][j] == self.settings.grid[i+2][j-2]:
                        self._color_error_box(i, j, i+2, j-2)
        
        #Top Middle Box
        for i in range(1,9,3):
            for j in range(0,9,3):
                if self.settings.grid[i][j] != '':
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j+1]:
                        self._color_error_box(i, j, i+1, j+1)
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j+2]:
                        self._color_error_box(i, j, i+1, j+2)

        #Center Middle Box
        for i in range(1,9,3):
            for j in range(1,9,3):
                if self.settings.grid[i][j] != '':
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j-1]:
                        self._color_error_box(i, j, i+1, j-1)
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j+1]:
                        self._color_error_box(i, j, i+1, j+1)

        #Bottom Middle Box
        for i in range(1,9,3):
            for j in range(2,9,3):
                if self.settings.grid[i][j] != '':
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j-1]:
                        self._color_error_box(i, j, i+1, j-1)
                    if self.settings.grid[i][j] == self.settings.grid[i+1][j-2]:
                        self._color_error_box(i, j, i+1, j-2)
                            


    def _color_error(self, i, x, y):
        if self.settings.grid[i][x] == self.settings.grid[i][y] and self.settings.grid[i][x] != '' and self.settings.grid[i][y] != '':
            text = self.settings.font.render(self.settings.grid[i][x], 1, RED)
            self.screen.blit(text, (i*100 + 30, x*100 + 20))
            text = self.settings.font.render(self.settings.grid[i][y], 1, RED)
            self.screen.blit(text, (i*100 + 30, y*100 + 20))
            print("here1")
            self.settings.hasError = True
        
        if self.settings.grid[x][i] == self.settings.grid[y][i] and self.settings.grid[x][i] != '' and self.settings.grid[y][i] != '':
            text = self.settings.font.render(self.settings.grid[x][i], 1, RED)
            self.screen.blit(text, (x*100 + 30, i*100 + 20))
            text = self.settings.font.render(self.settings.grid[y][i], 1, RED)
            self.screen.blit(text, (y*100 + 30, i*100 + 20))
            print("here2")
            self.settings.hasError = True

    def _color_error_box(self, x1, y1, x2, y2):
        print('box')
        text = self.settings.font.render(self.settings.grid[x1][y1], 1, RED)
        self.screen.blit(text, (x1*100 + 30, y1*100 + 20))
        text = self.settings.font.render(self.settings.grid[x2][y2], 1, RED)
        self.screen.blit(text, (x2*100 + 30, y2*100 + 20))
        self.settings.hasError = True
        

if __name__ == '__main__':
    #Make game instance and run game
    ai = Sudoku()
    ai.run_game()

