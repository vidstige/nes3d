import numpy as np


def normalized(a, axis=-1, order=2):
    n = np.atleast_1d(np.linalg.norm(a, order, axis))
    return a / n


def is_comment(line: str) -> bool:
    return line.startswith('#')


class Model(object):
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

    def _face_normal(self, face) -> np.array:
        p0, p1, p2 = [self.vertices[i] for i in face]
        return normalized(np.cross(p2 - p0, p1 - p0))

    def compute_face_normals(self):
        self.face_normals = [self._face_normal(f) for f in self.faces]
        
    @staticmethod
    def load_obj(path: str) -> 'Model':
        vertices = []
        faces = []
        with open(path) as f:
            for line in f:
                if is_comment(line):
                    continue
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'v':
                    vertices.append([float(x) for x in parts[1:]])
                if parts[0] == 'f':
                    faces.append([int(x) - 1 for x in parts[1:]])

        return Model(np.array(vertices), faces)


def edge_function(p0, p1, p2):
    ''' Calculates the signed area of the triangle (p0, p1, p2).
        The sign of the value tells which side of the line p0p1 that p2 lies.
        Defined as the cross product of <p2-p0> and <p1-p0>
    '''
    return (p2.x - p0.x) * (p1.y - p0.y) - (p2.y - p0.y) * (p1.x - p0.x)


def contains_point(p0, p1, p2, p):
    ''' Calculates the barycentric coordinates of the given point.
        Returns true if the point is inside this triangle,
        along with the color of that point calculated by interpolating the color
        of the triangle's vertices with the barycentric coordintes.
        Also returns the z-value of the point interpolated from the triangle's vertices.
    '''
    area = edge_function(p0, p1, p2)
    w0 =  edge_function(p1, p2, p)
    w1 = edge_function(p2, p0, p)
    w2 = edge_function(p0, p1, p)

    if area == 0: return False

    # Barycentric coordinates are calculated as the areas of the three sub-triangles divided
    # by the area of the whole triangle.
    alpha = w0 / area
    beta = w1 / area
    gamma = w2 / area

    return alpha >= 0 and beta >= 0 and gamma >= 0
    # This point lies inside the triangle if w0, w1, and w2 are all positive
    #if alpha >= 0 and beta >= 0 and gamma >= 0:
    #    # Interpolate the color of this point using the barycentric values
    #    red = int(alpha*self.p0.color.r() + beta*self.p1.color.r() + gamma*self.p2.color.r())
    #    green = int(alpha*self.p0.color.g() + beta*self.p1.color.g() + gamma*self.p2.color.g())
    #    blue = int(alpha*self.p0.color.b() + beta*self.p1.color.b() + gamma*self.p2.color.b())
    #    alpha = int(alpha*self.p0.color.a() + beta*self.p1.color.a() + gamma*self.p2.color.a())

        # Also interpolate the z-value of this point
    #    zValue = int(alpha*self.p0.z + beta*self.p1.z + gamma*self.p2.z)

    #    return True, Color(red, green, blue, alpha), zValue

    #return False, None, None

class RenderTarget(object):
    def __init__(self, img: np.array):
        self.img = img

    def pixel(self, x, y, color):
        width, height, _ = self.img.shape
        self.img[int(width/2 + x * width/2), int(height/2 - y*height/2)] = color

    def triangle(self, p0, p1, p2):
        width, height = self.img.shape
        # First calculate a bounding box for this triangle so we don't have to iterate over the entire image
        # Clamped to the bounds of the image
        xmin = max(min(p0.x, p1.x, p2.x), 0)
        xmax = min(max(p0.x, p1.x, p2.x), width)
        ymin = max(min(p0.y, p1.y, p2.y), 0)
        ymax = min(max(p0.y, p1.y, p2.y), height)

        # Iterate over all pixels in the bounding box, test if they lie inside in the triangle
        # If they do, set that pixel with the barycentric color of that point
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                point_in_triangle, color, zValue = self.contains_point(Point(x, y, color=None))
                if point_in_triangle:
                    # Check z-buffer to determine whether to draw this pixel
                    if zBuffer[y*image.width + x] < zValue:
                        zBuffer[y*image.width + x] = zValue
                        image.setPixel(x, y, color)


def render(img: np.array, model: Model, projection: np.array):
    screen = projection * np.vstack((model.vertices.T, np.ones((1,12))))
    target = RenderTarget(img)
    #for face in model.faces:

        #target.triang()

    for s in screen.T:
        x, y, z, w = s[0,0], s[0,1], s[0,2], s[0,3]
        target.pixel(x, y, color=(255, 0, 255, 255))
    

