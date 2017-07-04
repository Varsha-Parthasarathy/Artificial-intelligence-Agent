
# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
import PIL
from PIL import Image
from PIL import ImageChops
import numpy as np
from PIL import ImageMath

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    
    def checkError(self, im1, im2):
        diff = sum(abs(pix1 - pix2) for pix1, pix2 in zip(im1.getdata(), im2.getdata()))
        im_size = im1.size[0] * im1.size[1]
        return (diff * 100) / (255.0 * im_size)

     


    def LeftRightReflection(self, optA, optB, optC, soln_choices):
        error_lim = 3.0
        i = 1
        best_er = float('Inf')
        best_soln = -1
        if self.checkError(optA.transpose(Image.FLIP_LEFT_RIGHT), optB) < error_lim:
            for soln in soln_choices:
                if self.checkError(optC.transpose(Image.FLIP_LEFT_RIGHT), soln) < error_lim:
                    if self.checkError(optC.transpose(Image.FLIP_LEFT_RIGHT), soln) < best_er:
                        best_er = self.checkError(optC.transpose(Image.FLIP_LEFT_RIGHT), soln)
                        best_soln = i
                i += 1
        return best_soln



    def TopBottomReflection(self, optA, optB, optC, soln_choices):
        error_lim = 3.0
        i = 1
        best_er = float('Inf')
        best_soln = -1
        if self.checkError(optA.transpose(Image.FLIP_TOP_BOTTOM), optB) < error_lim:
            for soln in soln_choices:
                if self.checkError(optC.transpose(Image.FLIP_TOP_BOTTOM), soln) < error_lim:
                    if self.checkError(optC.transpose(Image.FLIP_TOP_BOTTOM), soln) < best_er:
                        best_er = self.checkError(optC.transpose(Image.FLIP_TOP_BOTTOM), soln)
                        best_soln = i
                i += 1
        return best_soln

        
    def Identical_2(self, optA, optB, optC, soln_choices):
        error_lim = 1.0
        i = 1
        best_er = float('Inf')
        best_soln = -1
        if self.checkError(optA, optB) < error_lim:
            for soln in soln_choices:
                if self.checkError(optC, soln) < error_lim:
                    if self.checkError(optC, soln) < best_er:
                        best_er = self.checkError(optC, soln)
                        best_soln = i
                i += 1
        return best_soln

                       

    def AddorDeleteAtoB(self, optA, optB, optC, soln_choices):
        error_lim = 4.5
        i = 1
        best_er = float('Inf')
        best_soln = -1
        for soln in soln_choices:
            if self.checkError(ImageChops.difference(optC, ImageChops.difference(optA, optB)), soln) < error_lim:
                if self.checkError(ImageChops.difference(optC, ImageChops.difference(optA, optB)), soln) < best_er:
                    best_er = self.checkError(ImageChops.difference(optC, ImageChops.difference(optA, optB)), soln)
                    best_soln = i
            i += 1
        return best_soln


    def AddorDeleteAtoC(self, optA, optB, optC, soln_choices):
        error_lim = 4.5
        i = 1
        best_er = float('Inf')
        best_soln = -1
        for soln in soln_choices:
            if self.checkError(ImageChops.difference(optB, ImageChops.difference(optA, optC)), soln) < error_lim:
                if self.checkError(ImageChops.difference(optB, ImageChops.difference(optA, optC)), soln) < best_er:
                    best_er = self.checkError(ImageChops.difference(optB, ImageChops.difference(optA, optC)), soln)
                    best_soln = i
            i += 1
        return best_soln
        

    def Rotation(self, optA, optB, optC, soln_choices, theta, best_er, best_soln):
        error_lim = 4.5
        i = 1
        if self.checkError(optA.rotate(theta), optB) < error_lim:
            for soln in soln_choices:
                if self.checkError(optC.rotate(theta), soln) < error_lim:
                    if self.checkError(optC.rotate(theta), soln) < best_er:
                        best_er = self.checkError(optC.rotate(theta), soln)
                        best_soln = i
                i += 1
        return best_soln
    
    


    def generator(self, optA, optB, optC, opt1, opt2, opt3, opt4, opt5, opt6):
        soln_choices = list((opt1, opt2, opt3, opt4, opt5, opt6))

        # Identical objects
        if self.checkError(optA, optB) <= self.checkError(optA, optC):
            ret_soln = self.Identical_2(optA, optB, optC, soln_choices)
        else:
            ret_soln = self.Identical_2(optA, optC, optB, soln_choices)

        if ret_soln != -1:
            return [ret_soln]

        ret_soln_choices = []

        #Left Right Reflection
        if self.checkError(optA.transpose(Image.FLIP_LEFT_RIGHT), optB) <= self.checkError(optA.transpose(Image.FLIP_LEFT_RIGHT), optC):
            ret_soln = self.LeftRightReflection(optA, optB, optC, soln_choices)
        else:
            ret_soln = self.LeftRightReflection(optA, optC, optB, soln_choices)
        if ret_soln != -1:
            ret_soln_choices.append(ret_soln)

        #Top Bottom Reflection   
        if self.checkError(optA.transpose(Image.FLIP_TOP_BOTTOM), optB) <= self.checkError(optA.transpose(Image.FLIP_TOP_BOTTOM), optC):
            ret_soln = self.TopBottomReflection(optA, optB, optC, soln_choices)
        else:
            ret_soln = self.TopBottomReflection(optA, optC, optB, soln_choices)
        if ret_soln != -1:
            ret_soln_choices.append(ret_soln)

        error_lim = 4.5
        
        #Add or Delete between A, B
        ret_soln = self.AddorDeleteAtoC(optA, optB, optC, soln_choices)
        if ret_soln != -1:
            ret_soln_choices.append(ret_soln)

        #Add or Delete between A, B
        ret_soln = self.AddorDeleteAtoB(optA, optB, optC, soln_choices)
        if ret_soln != -1:
            ret_soln_choices.append(ret_soln)

        #Rotation A, B
        best_er = float('Inf')
        best_soln = -1
        ret_list = []
        for theta in range(90, 360, 90):
            if self.checkError(optA.rotate(theta), optB) <= self.checkError(optA.rotate(theta), optC):
                ret_soln = self.Rotation(optA, optB, optC, soln_choices, theta, best_er, best_soln)
            else:
                ret_soln = self.Rotation(optA, optC, optB, soln_choices, theta, best_er, best_soln)
            if ret_soln != -1:
                ret_list.append(ret_soln)

        ret_soln = self.tester(ret_list)
        if ret_soln != -1:
            ret_soln_choices.append(ret_soln)


        return ret_soln_choices


    
    def tester(self, ret_soln_choices):
        if len(ret_soln_choices) > 0:
            return max(ret_soln_choices, key = ret_soln_choices.count)
        else:
            return -1   
   
   
   
   
    def Identical (self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):
    
        error_lim = 1.5
        A=self.Diff_img(figA, figB)
        B=self.Diff_img(figA, figD)
        C=self.Diff_img(figB, figC)
        D=self.Diff_img(figD, figG)
        if A <= B and C <= D:
            if A < error_lim and C < error_lim:
                for k, opt in enumerate(soln_choices):
                    P=self.Diff_img(figH, opt)
                    if P < error_lim:
                        return (k + 1)
        else:
            if B < error_lim and D < error_lim:
                for k, opt in enumerate(soln_choices):
                    Q=self.Diff_img(figH, opt)
                    if Q < error_lim:
                        return (k + 1)
        return -1


    def Getpixel(self, figA, figB, figC):
        Margin = lambda x : abs(x) < 2 
        pixA = self.no_of_pixels(ImageChops.invert(figA)) 
        pixB = self.no_of_pixels(ImageChops.invert(figB)) 
        pixC = self.no_of_pixels(ImageChops.invert(figC))
        A=(pixB - pixA)
        return Margin(pixC - pixB - A)


    def Scale(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):    

        if self.Getpixel(figA, figB, figC):
            for k, opt in enumerate(soln_choices):
                if self.Getpixel(figG, figH, opt):
                    return (k + 1)
        elif self.Getpixel(figA, figD, figG):
            for k, opt in enumerate(soln_choices):
                if self.Getpixel(figC, figF, opt):
                    return (k + 1)
        return -1



    def img_union (self, figA, figB):
        A= ImageChops.invert(figA)
        B= ImageChops.invert(figB)
        C= ImageChops.add(A,B)
        return ImageChops.invert(C)


    def Intersect(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):
        error_lim = 2.0
        X=self.img_union (figD, figB)
        Y=self.img_union (figD, figC)
        Z=self.img_union (figG, figB)
        A=self.Diff_img(X, figE) 
        B=self.Diff_img(Y, figF) 
        C=self.Diff_img(Z, figH)
        if A < error_lim and B < error_lim and C < error_lim:
            for k, opt in enumerate(soln_choices):
                P=self.img_union (figG, figC)
                Q=self.Diff_img(P,opt)
                if Q < error_lim:
                    return (k + 1)
        return -1


    def reflections(self, figA, figB, figC, figD, figE, figF, figG, figH):
        error_lim = 3.0
        below_limit = lambda x: x < error_lim
        A=self.Diff_img(figD.transpose(Image.FLIP_LEFT_RIGHT), figF)
        B=below_limit(A)
        C=self.Diff_img(figA.transpose(Image.FLIP_LEFT_RIGHT), figC)
        D=below_limit(C)
        E=self.Diff_img(figA.transpose(Image.FLIP_TOP_BOTTOM), figG)
        F=below_limit(E)
        G=self.Diff_img(figB.transpose(Image.FLIP_TOP_BOTTOM), figH)
        H=below_limit(G)
        return B and D and F and H
        


    def Reflection(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):
        error_lim = 1.0
        if self.reflections(figA, figB, figC, figD, figE, figF, figG, figH):
            for k, opt in enumerate(soln_choices):
                A=figC.transpose(Image.FLIP_TOP_BOTTOM)
                B=self.Diff_img(A, opt)
                C=figG.transpose(Image.FLIP_LEFT_RIGHT)
                D=self.Diff_img(C,opt)
                if (B < error_lim):
                   if (D< error_lim):
                    return (k + 1)
        return -1


    def NewObject(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):
        error_lim = 2
        cost = 0
        cosm = 100
        optm = -1
        P=ImageChops.difference(figA, figB)
        Q=ImageChops.difference(figD, P)
        A=self.Diff_img(Q,figE)
        R=ImageChops.difference(figA, figC)
        S=ImageChops.difference(R,figD)
        B=self.Diff_img(S,figF)
        T=ImageChops.difference(figA, figB)
        U=ImageChops.difference(figG,T)
        C=self.Diff_img(U,figH)
        if A < error_lim and B <error_lim and C < error_lim:
            for k, opt in enumerate(soln_choices):
                D=ImageChops.difference(figA, figC)
                E=ImageChops.difference(figG,D)
                F=self.Diff_img(E,opt)
                if F < error_lim and F < cosm:
                    cosm = F
                    optm = (k + 1)               
        return optm



    def Diff_img(self, i1, i2):
        pairs = zip(i1.getdata(), i2.getdata())
        #sub=(abs(p1 - p2))
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
        ncomponents = i1.size[0] * i1.size[1] #* 3
        return (dif / 255.0 * 100) / ncomponents
        


    def no_of_pixels(self, i1):
        x=(i1.size[0] * i1.size[1])
        y=sum(i1.getdata())
        z=float(y/x)
        return z
        
    def pixel_count(self,i1):
        pixels = i1.getdata() 
        # get the pixels as a flattened sequence
        black_thresh = 20
        nblack = 0
        for pixel in pixels:
            if pixel < black_thresh:
                nblack += 1
        n = len(pixels)
        return nblack
        

    def CompareGH(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  
         Compare=self.Diff_img(figG,figH)
         if Compare<3:
             for k, opt in enumerate(soln_choices):
                 Compare1=self.Diff_img(opt,figH)
                 if Compare1<1:
                     return (k+1)
         return -1
         
    def CompareGH_all(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  

         Question_choices = list((figA,figB,figC,figD,figE,figF,figG,figH))  
         count=0         
         A=self.pixel_count(figG)
         B=self.pixel_count(figH)
         diff_pixel=(B-A)
         error_lim1= (diff_pixel+180)
         error_lim2= (diff_pixel-180)
         for k, opt in enumerate(soln_choices):
              count=0
              C=self.pixel_count(opt)
              D=(C-B)
              for j, choice in enumerate(Question_choices):
                  check = self.same(opt,choice)
                  count=count+check
              if D<error_lim1 and D>error_lim2 :
                  return (k+1)                 
              elif count==8:
                  return (k+1)            
         return -1
         
    def same(self,i1,i2):
        A=self.pixel_count(i1) 
        B=self.pixel_count(i2)
        D=abs(B-A)
        if D<130 :
           return 0
        return 1
    

    def bit_XOR (self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices): 
        
        Dual1 = np.asarray(figA.convert('RGB'))
        Dual2 = np.asarray(figB.convert('RGB'))
        xorAB = np.bitwise_xor(Dual1,Dual2)
        xorAB = Image.fromarray(xorAB, 'RGB') 
        Ans=ImageChops.invert(xorAB)
        AB=Ans.convert('L')
        A=self.pixel_count(AB)
        B=self.pixel_count(figC)
        Compare=self.Diff_img(figC,AB)
        Dual11 = np.asarray(figG.convert('RGB'))
        Dual21 = np.asarray(figH.convert('RGB'))
        xorGH = np.bitwise_xor(Dual11,Dual21)
        xorGH = Image.fromarray(xorGH, 'RGB') 
        Ans1=ImageChops.invert(xorGH)
        GH=Ans1.convert('L')
        AA=self.pixel_count(GH)
        if Compare<1:
            for k, opt in enumerate(soln_choices):
                C=self.pixel_count(opt)
                Compare1=self.Diff_img(opt,GH)
                if Compare1< 3.66:
                    return(k+1)
        return -1
    
    def Compare1AE(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):
         Compare=self.Diff_img(figA,figE)
         if Compare<3:
             for k, opt in enumerate(soln_choices):
                 Compare1=self.Diff_img(opt,figE)
                 if Compare1<1:
                     return (k+1)
                                
         return -1    
    
    def CompareAE(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  

         A=self.pixel_count(figA)
         B=self.pixel_count(figE)
         diff_pixel=abs(B-A)
         if diff_pixel<100:
            for k, opt in enumerate(soln_choices):
                C=self.pixel_count(opt)
                D=abs(B-C)
                if D<60:
                    return (k+1)
         return -1    
     
    def SubGH(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  
         D=self.pixel_count(figA)
         E=self.pixel_count(figB)
         F=self.pixel_count(figC)
         G=self.pixel_count(figG)
         H=self.pixel_count(figH)
         dif_pixelDE=abs(D-E)
         dif_pixelGH=abs(G-H)
         margin=abs(F-dif_pixelDE)
         error_lim11= (dif_pixelDE+60)
         error_lim21= (dif_pixelDE-50)
         error_lim12= (dif_pixelGH+50)
         error_lim22= (dif_pixelGH-50)
         if (F<error_lim11 and F>error_lim21):
             for k, opt in enumerate(soln_choices):
                   C=self.pixel_count(opt)
                   if C<error_lim12 and C>error_lim22 :
                       return (k+1)
         return -1         
    
    def Sub1GH(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  
         Ans=ImageChops.difference(figB,figA)
         Ans1=ImageChops.invert(Ans)
         Compare=self.Diff_img(Ans1,figC)
         if Compare<2:
            for k, opt in enumerate(soln_choices):
                GH=ImageChops.difference(figH,figG)
                GH_1=ImageChops.invert(GH)
                C=self.pixel_count(opt)
                Compare1=self.Diff_img(opt,GH_1)
                if Compare1< 3.66:
                    return(k+1)

         return -1     
         
    def Add1GH(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  
         Ans=ImageChops.add(figB,figA)
         Ans1=ImageChops.invert(Ans)
         Compare=self.Diff_img(Ans,figC)
         if Compare<1:
            for k, opt in enumerate(soln_choices):
                GH=ImageChops.add(figH,figG)
                GH_1=ImageChops.invert(GH)
                C=self.pixel_count(opt)
                Compare1=self.Diff_img(opt,GH)
                if Compare1< 3.66:
                    return(k+1)

         return -1          
    
    def AddGH(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):  
         D=self.pixel_count(figD)
         E=self.pixel_count(figE)
         F=self.pixel_count(figF)
         G=self.pixel_count(figG)
         H=self.pixel_count(figH)
         sum_pixelDE=abs(D+E)
         sum_pixelGH=abs(G+H)
         error_lim11= (sum_pixelDE+130)
         error_lim21= (sum_pixelDE-130)
         error_lim12= (sum_pixelGH+750)
         error_lim22= (sum_pixelGH-750)
         if F<error_lim11 and F>error_lim21 :
             for k, opt in enumerate(soln_choices):
                   C=self.pixel_count(opt)
                   if C<error_lim12 and C>error_lim22 :
                       return (k+1)
         return -1         
             
         
         
         
   
    def Compareall(self, figA, figB, figC, figD, figE, figF, figG, figH, soln_choices):
        Question_choices = list((figA,figB,figC,figD,figE,figF,figG,figH))  
        count=0
        for k, opt in enumerate(soln_choices):
            count=0
            
            for j, choice in enumerate(Question_choices):
                check = self.same(opt,choice)
                count=count+check
                if count==8:
                    return (k+1)  
        return -1    
        

    def Solve(self,problem):
        
        if (problem.problemType == '2x2'):
            
            optA = Image.open(problem.figures['A'].visualFilename).convert('L')
            optB = Image.open(problem.figures['B'].visualFilename).convert('L')
            optC = Image.open(problem.figures['C'].visualFilename).convert('L')
            opt1 = Image.open(problem.figures['1'].visualFilename).convert('L')
            opt2 = Image.open(problem.figures['2'].visualFilename).convert('L')
            opt3 = Image.open(problem.figures['3'].visualFilename).convert('L')
            opt4 = Image.open(problem.figures['4'].visualFilename).convert('L')
            opt5 = Image.open(problem.figures['5'].visualFilename).convert('L')
            opt6 = Image.open(problem.figures['6'].visualFilename).convert('L')
        
            ret_soln_choices = self.generator(optA, optB, optC, opt1, opt2, opt3, opt4, opt5, opt6)
            final_ret_soln = self.tester(ret_soln_choices)
            print (final_ret_soln)
            print (problem.name)
            return final_ret_soln
        
        elif(problem.problemType == '3x3'):

                
            figA = Image.open(problem.figures['A'].visualFilename).convert('L')
            figB = Image.open(problem.figures['B'].visualFilename).convert('L')
            figC = Image.open(problem.figures['C'].visualFilename).convert('L')
            figD = Image.open(problem.figures['D'].visualFilename).convert('L')
            figE = Image.open(problem.figures['E'].visualFilename).convert('L')
            figF = Image.open(problem.figures['F'].visualFilename).convert('L')
            figG = Image.open(problem.figures['G'].visualFilename).convert('L')
            figH = Image.open(problem.figures['H'].visualFilename).convert('L')

            
            Opt1 = Image.open(problem.figures['1'].visualFilename).convert('L')
            Opt2 = Image.open(problem.figures['2'].visualFilename).convert('L')
            Opt3 = Image.open(problem.figures['3'].visualFilename).convert('L')
            Opt4 = Image.open(problem.figures['4'].visualFilename).convert('L')
            Opt5 = Image.open(problem.figures['5'].visualFilename).convert('L')
            Opt6 = Image.open(problem.figures['6'].visualFilename).convert('L')
            Opt7 = Image.open(problem.figures['7'].visualFilename).convert('L')
            Opt8 = Image.open(problem.figures['8'].visualFilename).convert('L')

            soln_choices= list((Opt1, Opt2, Opt3, Opt4, Opt5, Opt6, Opt7, Opt8))
            Question_choices = list((figA,figB,figC,figD,figE,figF,figG,figH))
#            print (problem.name)
            #sol_num=[self.CompareGH_all]
            #original self.NewObject,self.AddGH,self.SubGH,
            sol_num=[self.Reflection,self.Identical,self.Intersect,self.Sub1GH,self.Add1GH,self.SubGH,self.CompareAE,self.CompareGH_all]
            #sol_num = [self.Sub1GH,self.Add1GH,self.SubGH,self.CompareAE,self.CompareGH_all]
            #sol_num = [self.Sub1GH,self.Add1GH,self.SubGH]
            soln_returned  = []
            
            for i, f in enumerate(sol_num):
                Score = f(figA, figB, figC, figD, figE, figF, figG, figH, soln_choices)
                if Score != -1:
                    soln_returned .append(Score)
            
            if len(soln_returned ) > 0:
                #print (soln_returned)
                #print(max(soln_returned , key = soln_returned .count))
                return max(soln_returned , key = soln_returned .count)
            else:
                return -1

        else:
            return -1