import abc

class Experiment(abc.ABC):
    
    @abc.abstractmethod
    def query_function(df, session_id, experiment, test_id, questions, item):
        pass
    
    @abc.abstractmethod
    def _format_table(table_data):
        pass
    
    @abc.abstractmethod
    def _create_document(data):
        pass
    
    