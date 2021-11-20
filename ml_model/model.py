import fasttext
import re
import argparse

class Bullying():
    def __init__(self, model_path):
        self.model = fasttext.load_model(model_path)
        self.label = ['Offensive', 'Compliment']

    def clean_text(self, text):
        # filter to allow only alphabets
        text = re.sub(r'[^a-zA-Z\']', ' ', text)
        
        # remove Unicode characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        # convert to lowercase to maintain consistency
        text = text.lower()
        
        return text

    def predict(self, statement):
        input_statement = self.clean_text(statement)
        prediction = self.model.predict(input_statement)[0][0]
        return self.label[int(prediction[-1])]
        

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--statement', required=True,
                        help="Statement that needs to be evaluated")
    args = vars(parser.parse_args())

    bullying = Bullying('model_bullying.bin')
    prediction = bullying.predict(args['statement'])

    print("The statement is evaluated as: ",prediction)
