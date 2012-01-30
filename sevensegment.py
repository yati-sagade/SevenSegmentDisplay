'''
Created on Jan 28, 2012

@author: yati
'''
import pygame
import pygame.gfxdraw
pygame.init()

A = 0x01
B = 0x02
C = 0x04
D = 0x08
E = 0x10
F = 0x20
G = 0x40

def segments(*args):
    '''
    takes the segment codes of segments that must be ON, and returns an
    appropriate int by logically ORing all the supplied codes
    '''
    return reduce(lambda x, y: (x | y), args, 0)

ALL = segments(A, B, C, D, E, F, G)

# Sometimes, it is nicer to specify which segments should be off.
def off_segments(*args):
    '''
    takes the segments that are to remain off, and returns an appropriate value
    '''
    return (ALL & (~ segments(*args)))
    
        
# This map could as well have used sets, but I decided to stick to bit twiddling.
SSD_CHAR_MAP = {
                '0': segments(A, B, C, D, E, F),
                '1': segments(B, C),
                '2': segments(A, B, D, E, G),
                '3': segments(A, B, C, D, G),
                '4': segments(B, C, G, F),
                '5': segments(A, C, D, F, G),
                '6': segments(A, C, D, E, F, G),
                '7': segments(A, B, C),
                '8': segments(A, B, C, D, E, F, G),
                '9': segments(A, B, C, D, F, G),
                
                 # SPACE
                ' ': off_segments(A, B, C, D, E, F, G),
                
                'A': off_segments(D),
                'B': off_segments(A, B),
                'C': segments(A, D, E, F),
                'D': off_segments(A, F),
                'E': off_segments(B, C),
                'F': off_segments(B, C, D),
                'G': off_segments(B, G),
                'H': off_segments(A, B, D),
                'I': segments(B, C),
                'J': off_segments(A, F, G),
                # K looks like a capital H, but that's the best we can do with
                # an SSD.
                'K': off_segments(A, D),
                'L': segments(D, E, F),
                 # write two Ns if you need an M.
                'N': off_segments(D, G),
                'O': off_segments(A, B, F),
                'P': off_segments(C, D),
                'Q': off_segments(D, E),
                'R': segments(E, G),
                'S': off_segments(B, E),
                'T': off_segments(A, B, C),
                'U': off_segments(A, G),
                'V': segments(C, D, E), # Actually looks like a u.
                 # W: use two Vs
                 # No X 
                'Y': off_segments(A, E),
                'Z': off_segments(C, F),
                }

# Add the keys for lowercase characters
for key in SSD_CHAR_MAP.keys():
    if key.lower() != key:
        SSD_CHAR_MAP[key.lower()] = SSD_CHAR_MAP[key]


class SevenSegmentChar(object):
        
    def __init__(self,
                 char,
                 colour=(255, 0, 0),
                 bgcolour=(0,0,0), 
                 width=7, 
                 height=17,
                 segment_width=2):
        '''
        ctor;
        takes the following args:
        char: The char to represent. This value must be a key in SSD_CHAR_MAP.
        colour: (R,G,B) colour tuple - default red.
        bgcolour: (R,G,B) triple for the background of this char - default black.
        width: width of this character in pixels - default is 7px.
        height: height of this character in pixels - default is 17px.
        segment_width: the width of each segement in the char - default is 2px.
        '''
        assert char in SSD_CHAR_MAP
        self._char = char
        self._width = width
        self._colour = colour
        self._bgcolour = bgcolour
        self._segment_width = segment_width
        self._segment_length = self._width - 2 * self._segment_width
        self._height = 2 * self._segment_length + 3 * self._segment_width
        self._surface = pygame.Surface((self._width, self._height))
        self._surface.fill(bgcolour)
        
        segment_point_pairs = self._get_segment_points()
        for point_pair in segment_point_pairs:
            print(point_pair)
            if point_pair:
                pygame.draw.line(self._surface,
                                 self._colour,
                                 point_pair[0], 
                                 point_pair[1],
                                 self._segment_width
                               )
        
        
    def _get_segment_points(self):
        '''
        returns an iterable of point pairs which denote the start and end points
        of each segment, in order from A to G. A value of None, [], or () should 
        be treated as an unlit segment.
        '''
        xmin = self._segment_width
        xmax = self._segment_width + self._segment_length
        
        ymin = self._segment_width
        ymax = 2 * self._segment_length + 2 * self._segment_width
         
        slen = self._segment_length
        
        positions = {
                     A: ((xmin, ymin),
                         (xmax, ymin)),
                     
                     B: ((xmax, ymin),
                         (xmax, ymin + slen)),
                     
                     C: ((xmax, ymax - slen),
                         (xmax, ymax)),
                     
                     D: ((xmax, ymax),
                         (xmin, ymax)),
                     
                     E: ((xmin, ymax), 
                         (xmin, ymax - slen)),
                     
                     F: ((xmin, ymin),
                         (xmin, ymin + slen)),
                     
                     G: ((xmin, ymin + slen),
                         (xmax, ymin + slen))}
        
        ssd = SSD_CHAR_MAP[self._char]
        ret = []
        
        for segment in (A, B, C, D, E, F, G):
            if segment & ssd:
                ret.append(positions[segment])
            else:
                ret.append(None)
        
        return ret
    
    def update(self):
        self._segment_length = self._width - 2 * self._segment_width
        self._surface.fill(self._bgcolour)
        segment_point_pairs = self._get_segment_points()
        for point_pair in segment_point_pairs:
            if point_pair:
                pygame.draw.line(self._surface,
                                 self._colour,
                                 point_pair[0], 
                                 point_pair[1],
                                 self._segment_width
                                 )
            
    @property
    def surface(self):
        return self._surface
    
    @surface.setter
    def surface(self, new):
        self._surface = new
        self.update()
    
    @property
    def bgcolour(self):
        return self._bgcolour
    
    @bgcolour.setter
    def bgcolour(self, new):
        self._bgcolour = new
        self.update()
        
    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, new):
        self._colour = new
        self.update()
    
    @property
    def char(self):
        return self._char
    
    @char.setter
    def char(self, new):
        assert new in SSD_CHAR_MAP
        self._char = new
        self.update()
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, new):
        self._width = new
        self.update()
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, new):
        self._height = new
        self.update()
    
    @property
    def segment_width(self):
        return self._segment_width
    
    @segment_width.setter
    def segment_width(self, new):
        self._segment_width = new
        self.update()

class SevenSegmentDisplay(list):
    '''
    The main display class - acts a a container for SevenSegmentChar objects.
    '''
    def __init__(self,
                 width,
                 height,
                 content='',
                 colour=(255,0,0), # red
                 bgcolour=(0,0,0), # black
                 segment_width=2, 
                 char_width=None, 
                 right_justify=True):
        '''
        ctor for SevenSegmentDisplay. 
        Args:
            width: width of this panel.
            
            height: height of this panel.
            
            content: a string representing the content of the panel.
            
            colour: colour of the lit up segments. default red.
            
            bgcolour: background of the display. default black.
            
            segment_width: width of a segment in pixels. default 2px.
            
            char_width: width of each character - If not given, this value is
                calculated from `width` and len(content). If given, this width is
                used even if space in the panel is unused.
            
            right_justify: If this is True(default), the content is displayed right
                justified, as in traditional SSD displays. Otherwise, content is
                displayed left justified(surprise!!)
        '''
        self._width = width
        self._height = height
        self._content = content
        self._colour = colour
        self._bgcolour = bgcolour
        self._segment_width = segment_width
        self._right_justified = right_justify
        
        if char_width:
            self._char_width = char_width
        else:
            if not content:
                raise ValueError('Empty content and no char_width')
            
            self._char_width = int(self._width / len(self._content))
        
        self._surface = pygame.Surface((self._width, self._height))
        self._numchars = int(self._width / self._char_width)
        self.update()
    
    def update(self):
        self[:] = []
        self._numchars = int(self._width / self._char_width)
        for c in self._content:
            self.append(SevenSegmentChar(c,
                                         self._colour,
                                         self._bgcolour,
                                         self._char_width,
                                         self._height, 
                                         self._segment_width))
    
        self.update_surface()
    
    def update_surface(self):
        rect = pygame.Rect(0, 0, self._char_width, self._height)
        if self._right_justified:
            deficit = self._numchars - len(self._content)
            rect.move(deficit * self._char_width, 0)
            
        for ssdchar in self[-self._numchars:]:
            self._surface.blit(ssdchar.surface, rect)
            rect = rect.move(self._char_width, 0)
            
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, new):
        self._width = new
        self._surface = pygame.Surface(self._width, self._height)
        self.update()
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, new):
        self._height = new
        self._surface = pygame.Surface(self._width, self._height)
        self.update()
    
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, new):
        self._content = new[-self._numchars:]
        self.update()
    
    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, new):
        self._colour = new
        for ssdchar in self:
            ssdchar.colour = new
        
        self.update_surface()
    
    @property
    def bgcolour(self):
        return self._bgcolour
    
    @bgcolour.setter
    def bgcolour(self, new):
        self._bgcolour = new
        for ssdchar in self:
            ssdchar.bgcolour = new
        
        self.update_surface()
    
    @property
    def segment_width(self):
        return self._segment_width
    
    @segment_width.setter
    def segment_width(self, new):
        self._segment_width = new
        for ssdchar in self:
            ssdchar.segment_width = new
        
        self.update_surface()
    
    @property
    def char_width(self):
        return self._char_width
    
    @char_width.setter
    def char_width(self, new):
        self._char_width = new
        self.update()
    
    @property
    def right_justified(self):
        return self._right_justified
    
    @right_justified.setter
    def right_justified(self, new):
        self._right_justified = new
        self.update()
    
    @property
    def surface(self):
        return self._surface
    
    @surface.setter
    def surface(self, new):
        self._surface = new
        self._width = new.get_width()
        self._height = new.get_height()
        self.update()