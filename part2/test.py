import pylab

pylab.rcParams['lines.linewidth'] = 7
pylab.rcParams['axes.titlesize'] = 20
pylab.rcParams['axes.labelsize'] = 15

def findPayment(loan, r, m):
	""" assumes: loans and r are floats, m is int. Returns the monthly payment 
	for a mortgage of size loan at a monthly rate of r for m months """

	return loan*((r*(1+r)**m)/((1+r)**m - 1))

# Primary use of class classes as types and subclasses as a mechanism for defining subtypes
# mixin class: bundle together a set of related functions that dont constitute a type

class MortgagePlots(object):
	def plotPayments(self, style):
		pylab.plot(self.paid[1:], style, label = self.legend)

	def plotToPd(self, style):
		totPd = [self.paid[0]]
		for i in range(1, len(self.paid)):
			totPd.append(totPd[-1] + self.paid[i])
		pylab.plot(totPd, style, label = self.legend)

# multiple inheritance: because Mortgage inherits from both Mortgage Plots and Object
# be careful when use multiple inheritance, can be dangerous

class Mortgage(MortgagePlots, object):
	""" Abstract class for building different kinds of mortgages """
	def __init__(self, loan, annRate, months):
		""" Create a new mortgage """
		self.loan = loan
		self.rate = annRate/12.0
		self.months = months
		self.paid = [0.0]
		self.owed = [loan]
		self.payment = findPayment(loan, self.rate, months)

	def makePayment(self):
		""" Make a payment """
		self.paid.append(self.payment)
		reduction = self.payment - self.owed[-1] * self.rate
		self.owed.append(self.owed[-1] - reduction)

	def getTotalPaid(self):
		""" Return the total amount paid so far """
		return sum(self.paid)

	def __str__(self):
		return self.legend

class Fixed(Mortgage):
	def __init__(self, loan, r, months):
		Mortgage.__init__(self, loan, r, months)
		self.legend = 'Fixed, ' + str(r*100) + '%'


class FixedWithPts(Fixed):
	def __init__(self, loan, r, months, pts):
		Fixed.__init__(self, loan, r, months)
		self.pts = pts
		self.paid = [loan*(pts/100.0)]
		self.legend += ', ' + str(pts) + ' points'

class TwoRate(Mortgage):
        def __init__(self,loan,r,months,teaserRate,teaserMonths):
                Mortgage.__init__(self,loan,teaserRate,months)
                self.teaserMonths = teaserMonths
                self.teaserRate = teaserRate
                self.nextRate = r/12
                self.legend = str(teaserRate*100) + '% for' + str(self.teaserMonths) + ' months, then ' + str(r*100) + '%'

        def makePayment(self):
                if len(self.paid) == self.teaserMonths +1:
                        self.rate = self.nextRate
                        self.payment = findPayment(self.owed[-1], self.rate, self.months - self.teaserMonths)
                Mortgage.makePayment(self)
                


def plotMortgages(morts, amt):
	styles = ['b-', 'r-.', 'g:']
	payments = 0
	cost = 1
	pylab.figure(payments)
	pylab.title('Monthly Payments of Different $' +str(amt) + ' Mortgages')
	pylab.xlabel('Months')
	pylab.ylabel('Monthly Payments')
	pylab.figure(cost)
	pylab.title('Cost of Difference $' + str(amt) + ' Mortgages')
	pylab.xlabel('Months')
	pylab.ylabel('Total Payments')
	for i in range(len(morts)):
		pylab.figure(payments)
		morts[i].plotPayments(styles[i])
		pylab.figure(cost)
		morts[i].plotToPd(styles[i])
	pylab.figure(payments)
	pylab.legend(loc = 'upper center')
	pylab.figure(cost)
	pylab.legend(loc = 'best')

def compareMortgages(amt, years, fixedRate, pts, ptsRate, varRate1, varRate2, varMonths):
	totMonths = years *12
	fixed1 = Fixed(amt, fixedRate, totMonths)
	fixed2 = FixedWithPts(amt, ptsRate, totMonths, pts)
	twoRate = TwoRate(amt, varRate2, totMonths, varRate1, varMonths)
	morts = [fixed1, fixed2, twoRate]
	for m in range(totMonths):
		for mort in morts:
			mort.makePayment()
	plotMortgages(morts, amt)

compareMortgages(amt=200000, years=30, fixedRate=0.07,
                 pts = 3.25, ptsRate=0.05, varRate1=0.045,
                 varRate2=0.095, varMonths=48)

pylab.show()

