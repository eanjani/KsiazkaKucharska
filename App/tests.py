from django.test import TestCase
from klasyfikacja import classifyText

sources = { 
        18:'ciasto',
        19:'ciasto',
        20:'ciasto',
        25:'deser',
        32:'ciasto',
        31:'ciasto',
        38:'deser',
        46:'deser',
        50:'deser',
        52:'deser'
    }

# Create your tests here.
class ClassificationTestCase(TestCase):

    def testClassification(self):
        for id, typ in sources.items():
            print id," : ",classifyText(str(id))
            self.assertEqual(classifyText(str(id)), typ)

    def testWrongClassification(self):
        self.assertNotEqual(classifyText(str(18)), 'deser')
        self.assertNotEqual(classifyText(str(52)), 'ciasto')