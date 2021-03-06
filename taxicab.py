import rhinoscriptsyntax as rs
from Rhino.Geometry import Point3d as P3
from Rhino.Geometry import Polyline as PLine

def taxicab_midnormal ( Point_1 = P3(0,0,0), Point_2 = P3(0,0,0) , leng = 10000):
    dx = abs(Point_1.X - Point_2.X)
    dy = abs(Point_1.Y - Point_2.Y)
    
    C = P3 ( ( Point_1.X + Point_2.X ) / 2, ( Point_1.Y + Point_2.Y ) / 2, ( Point_1.Z + Point_2.Z ) / 2)
    
    """ MPQN, in which M is on the lengeft(X-) or bottom(Y-) """
    P = P3 (0,0,C.Z)
    Q = P3 (0,0,C.Z)
    M = P3 (0,0,C.Z)
    N = P3 (0,0,C.Z)
    
    if dx > dy:
        P.Y = C.Y + dy / 2
        Q.Y = C.Y - dy / 2
        M.Y = P.Y + leng
        N.Y = Q.Y - leng
        if bool(Point_1.Y > Point_2.Y) ^ bool(Point_1.X > Point_2.X):
            P.X = C.X + dy / 2
            Q.X = C.X - dy / 2
        else:
            P.X = C.X - dy / 2
            Q.X = C.X + dy / 2
        M.X = P.X
        N.X = Q.X
    else:
        if dx < dy:
            P.X = C.X + dx / 2
            Q.X = C.X - dx / 2
            M.X = P.X + leng
            N.X = Q.X - leng
            if bool(Point_1.Y > Point_2.Y) ^ bool(Point_1.X > Point_2.X):
                P.Y = C.Y + dx / 2
                Q.Y = C.Y - dx / 2
            else:
                P.Y = C.Y - dx / 2
                Q.Y = C.Y + dx / 2
            M.Y = P.Y
            N.Y = Q.Y
        else:
            if bool(Point_1.Y > Point_2.Y) ^ bool(Point_1.X > Point_2.X):
                P.Y = C.Y - dx / 2
                Q.Y = C.Y + dx / 2
                P.X = C.X - dy / 2
                Q.X = C.X + dy / 2
                M.Y = P.Y - leng
                M.X = P.X - leng
                N.Y = Q.Y + leng
                N.X = Q.X + leng
            else:
                P.Y = C.Y - dx / 2
                Q.Y = C.Y + dx / 2
                P.X = C.X + dy / 2
                Q.X = C.X - dy / 2
                M.Y = P.Y - leng
                M.X = P.X + leng
                N.Y = Q.Y + leng
                N.X = Q.X - leng

    return rs.AddPolyline( [M , P , Q , N] )

def taxicab_circle ( point = P3(0,0,0), r = 1 ):
    A = P3( point.X + r, point.Y, point.Z )
    B = P3( point.X, point.Y + r, point.Z )
    C = P3( point.X - r, point.Y, point.Z )
    D = P3( point.X, point.Y - r, point.Z )
    return rs.AddPolyline( [A, B, C, D, A] )

l = 2 * r

""" PL = taxicab_midnormal ( A, B, r ) """

pts = P

polylines = []

for pt in P:
    polylines.append(taxicab_circle(pt, r))

for i in range(len(polylines)):
    for j in range(i):
        if i == j:
            continue
        if rs.CurveBooleanUnion( [ polylines[i], polylines[j] ] ):
            MN = taxicab_midnormal( pts[i], pts[j], l )
            
            ccx = rs.CurveCurveIntersection( polylines[i], MN )
            if ccx is None:
                continue
            if ccx[0][0] == 2:
                continue
            para_a = [ ccx[0][5], ccx[1][5] ]
            para_b = [ ccx[0][7], ccx[1][7] ]
            
            if para_b[0] > para_b[1]:
                para_b = [ para_b[1], para_b[0] ]
            
            probable_dash = rs.SplitCurve(polylines[i], para_a)
            edge = rs.TrimCurve(MN, para_b, False )
            edgepts = rs.CurvePoints(edge)
            
            for crv in probable_dash:
                crvpts = rs.CurvePoints(crv)
                if rs.PointCompare( crvpts[0], edgepts[0] ):
                    crvpts.reverse()
                newpl = rs.AddPolyline( edgepts + crvpts )
                if rs.PointInPlanarClosedCurve( pts[i], newpl ):
                    polylines[i] = newpl
                    break
            
            
            ccx = rs.CurveCurveIntersection( polylines[j], MN )
            if ccx is None:
                continue
            para_a = [ ccx[0][5], ccx[1][5] ]
            para_b = [ ccx[0][7], ccx[1][7] ]
            
            if para_b[0] > para_b[1]:
                para_b = [ para_b[1], para_b[0] ]
            
            probable_dash = rs.SplitCurve(polylines[j], para_a)
            edge = rs.TrimCurve(MN, para_b, False )
            edgepts = rs.CurvePoints(edge)
            
            for crv in probable_dash:
                crvpts = rs.CurvePoints(crv)
                if rs.PointCompare( crvpts[0], edgepts[0] ):
                    crvpts.reverse()
                newpl = rs.AddPolyline( edgepts + crvpts )
                if rs.PointInPlanarClosedCurve( pts[j], newpl ):
                    polylines[j] = newpl
                    break
    

PL = polylines
