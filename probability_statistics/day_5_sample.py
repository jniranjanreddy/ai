# from scipy.stats import chi2_contingency

# # Contingency table example
# data = [[50, 30], [20, 40]]


# chin2, p, dof, expected = chi2_contingency(data)
# print("Chi-Square Stattitics:", chin2)
# print("P-Value:", p)
# print("Expected Frequencies:\n", expected)



#####################################
# ## ANOVA Test - Analysis of Variance
# ## One-way ANOVA example
from scipy.stats import f_oneway

group1 = [23, 21, 18, 30, 27]
group2 = [25, 29, 31, 22, 24]
group3 = [30, 28, 26, 32, 29]

f_stat, p_value = f_oneway(group1, group2, group3)
print("F-Statistic:", f_stat)
print("P-Value:", p_value)


f_stat, p_value = f_oneway(group1, group2)
print("F-Statistic:", f_stat)
print("P-Value:", p_value)# from scipy.stats import ttest_ind