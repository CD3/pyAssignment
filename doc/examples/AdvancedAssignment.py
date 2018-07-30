import os,sys
from pyAssignment.Assignment import Assignment
import pyAssignment.Assignment.Answers as Answer
from pyAssignment.Actions import BuildProblemSetAndBlackboardQuiz
import numpy
import pyErrorProp as err

uconv = err.UncertaintyConvention()
units = uconv._UNITREGISTRY
Q_ = units.Quantity
UQ_ = uconv.UncertainQuantity

units.define('electronvolt = 1.60217653e-19 * J = eV')


ass = Assignment()
ass.meta.title = r'Module 01 Homework'
ass.meta.header = dict()
ass.meta.header['L'] = r'Engineering Physics'
ass.meta.header['C'] = r''
ass.meta.header['R'] = r'Mod 01'
ass.meta.footer = dict()
ass.meta.footer['L'] = r'Last Updated: \today{} \currenttime{}'
ass.meta.footer['C'] = r''
ass.meta.footer['R'] = r'Powered by \LaTeX'
ass.meta.latex_preamble_lines = [r'\DeclareSIUnit \degF {\degree F}'
                                ,r'\DeclareSIUnit \degC {\degree C}'
                                ,r'\DeclareSIUnit \degK {K}'
                                ,r'\DeclareSIUnit \mile {mi}'
                                ,r'\DeclareSIUnit \inch {in}'
                                ,r'\DeclareSIUnit \foot {ft}'
                                ,r'\DeclareSIUnit \yard {yd}'
                                ,r'\DeclareSIUnit \acre {acre}'
                                ,r'\DeclareSIUnit \lightyear {ly}'
                                ,r'\DeclareSIUnit \year {yr}'
                                ,r'\DeclareSIUnit \parcec {pc}'
                                ,r'\DeclareSIUnit \teaspoon {tsp.}'
                                ,r'\DeclareSIUnit \tablespoon {tbsp.}'
                                ,r'\DeclareSIUnit \gallon {gal}'
                                ,r'\DeclareSIUnit \quart {qt}'
                                ,r'\DeclareSIUnit \pallet {pallet}'
                                ,r'\DeclareSIUnit \dollar {{\$}}'
                                ,r'\DeclareSIUnit \poundmass {lbm}'
                                ,r'\DeclareSIUnit \poundforce {lbf}'
                                ,r'\DeclareSIUnit \gravity {g}'
                                ,r'\DeclareSIUnit \revolutionsperminute{rpm}'
                                ,r'\DeclareSIUnit \mph{mph}'
                                ,r'\DeclareSIUnit \fluidounce{floz}'
                                ,r'\DeclareSIUnit \turn {rev}'
                                ]


with ass.add_question() as q:
  q.text = r'''The average distance between the electron and proton in a Hydrogen atom is {AverageRadius:.2fLx}.'''
  # all variables declared in the q.NS namespace are automatically
  # available in the question test using the python format syntax.
  # i.e. q.NS.VAR -> {VAR}
  # pint quantities support latex formatting with the ':Lx' format spec
  q.NS.AverageRadius = Q_(52.9177,'pm')*1.5 # 1.5 times the Borh radius

  with q.add_question() as qq:
    qq.text = r'''What is the average distance between the proton and electron?'''
    with qq.add_answer(Answer.Numerical) as a:
      a.quantity = q.NS.AverageRadius.to('m')

  with q.add_part() as p:
    p.text = r'''Compute the magnitude of the electrostatic force between the electron and proton at this distance.'''

    # a function to compute the force.
    # error will be automatically propagated.
    @uconv.WithAutoError()
    def CalcForce(AverageRadius):
      # 
      r = AverageRadius
      q_p = Q_(1.602e-19,'C')
      q_e = -q_p
      k = Q_(8.99e-9,'N m^2 / C^2')

      F = abs(k*q_p*q_e / r**2)

      return F.to("N")

    with p.add_question() as qq:
      qq.text = r'''What is the magnitude of the force?'''
      with qq.add_answer(Answer.Numerical) as a:
        a.quantity = CalcForce # pyAssignment will automatically call CalcForce with the correct arguments from q.NS

  with q.add_part() as p:
    p.text = r'''Compute the electric potential of the Hydrogen atom in this configuration.'''

    @uconv.WithAutoError()
    def CalcPotentialEnergy(AverageRadius):
      r = AverageRadius
      q_p = Q_(1.602e-19,'C')
      q_e = -q_p
      k = Q_(8.99e-9,'N m^2 / C^2')

      U = k*q_p*q_e / r

      return U.to("eV")

    with p.add_question() as qq:
      qq.text = r'''What is the potential energy?'''
      with qq.add_answer(Answer.Numerical) as a:
        a.quantity = CalcPotentialEnergy


with ass.add_question() as q:
  text = r'''A charge $q_1 = {Charge:Lx}$ is placed in a uniform electric field of magnitude $E = {FieldMagnitude:Lx}$. The electric field makes an
             angle {FieldDirection:Lx} with the $+x$ axis.'''
  q.NS.Charge = Q_(-1,'nC')
  q.NS.FieldMagnitude = Q_(2.1,'V/m')
  q.NS.FieldDirection = Q_(104,'degree')

  def CalcForce(q,E,theta):
    F = q*E
    Fx = F*numpy.cos(theta)
    Fy = F*numpy.sin(theta)

    return Fx.to('N'),Fy.to('N')


  with q.add_part() as p:
    text = r'''Compute the $x$ component of the force exerted on the charge by the uniform field.'''
    @uconv.WithAutoError()
    def CalcXComponent(Charge,FieldMagnitude,FieldDirection):
      return CalcForce(Charge,FieldMagnitude,FieldDirection)[0].to('N')

    with p.add_question() as qq:
      qq.text = r'''What is the x component?'''
      with qq.add_answer(Answer.Numerical) as a:
        a.quantity = CalcXComponent

  with q.add_part() as p:
    text = r'''Compute the direction of the force exerted on the charge by the uniform field.'''
    @uconv.WithAutoError()
    def CalcDirection(Charge,FieldMagnitude,FieldDirection):
      F = CalcForce(Charge,FieldMagnitude,FieldDirection)
      theta = numpy.arccos( F[0] / (F[0]**2 + F[1]**2)**0.5 )

      return theta.to("degree")

    with p.add_question() as qq:
      qq.text = r'''What is the direction? Give your answer as a positive angle with respect to the +x axis.'''
      with qq.add_answer(Answer.Numerical) as a:
        a.quantity = CalcDirection


basename = os.path.basename(__file__).replace(".py","")
BuildProblemSetAndBlackboardQuiz(ass,basename,remove=False)
