#! -*- coding: utf-8 -*-
# 主要模型

import numpy as np
from my_bert.layers import *
from my_bert.snippets import delete_arguments
from keras.models import Model
import json


class Transformer(object):
    def __init__(self,
                 vocab_size,
                 hidden_size,
                 num_hidden_layers,
                 num_attention_heads,
                 intermediate_size,
                 hidden_act,
                 dropout_rate=None,
                 embedding_size=None,
                 attention_key_size=None,
                 sequence_length=None,
                 keep_tokens=None,
                 layers=None,
                 name=None,
                 **kwargs
                 ):
        if keep_tokens is None:
            self.vocab_size = vocab_size
        else:
            self.vocab_size = len(keep_tokens)
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.attention_head_size = hidden_size // num_attention_heads
        self.attention_key_size = attention_key_size or self.attention_head_size
        self.intermediate_size = intermediate_size
        self.hidden_act = hidden_act
        self.dropout_rate = dropout_rate or 0
        self.embedding_size = embedding_size or self.hidden_size
        self.sequence_length = sequence_length
        self.keep_tokens = keep_tokens
        self.attention_mask = None
        self.position_bias=None,
        self.layers = {} if layers is None else layers
        self.name = name
        self.built = False
        
    def build(self,
              layer_norm_cond=None,
              layer_norm_cond_hidden_size=None,
              layer_norm_cond_hidden_act=None,
              additional_input_layers=None,
              **kwargs):
        if self.built:
            return None
        
        inputs = self.get_inputs()
        self.set_inputs(inputs,additional_input_layers)
        
        self.layer_norm_conds = [
                                    layer_norm_cond,
                                    layer_norm_cond_hidden_size,
                                    layer_norm_cond_hidden_act or 'linear'
                              ]
        outputs = self.call(inputs)
        self.set_outputs(outputs)
        self.model = Model(self.inputs,self.outputs,name=self.name)
        self.built = True
    
    def call(self,inputs):
        outputs = self.apply_embeddings(inputs)
        for i in range(self.num_hidden_layers):
            outputs = self.apply_main_layers(outputs,i)
        outputs = self.apply_final_layers(outputs)
        return outputs
    
    def get_inputs(self):
        raise NotImplementedError
    
    def apply(self,inputs,layer=None,arguments=None,**kwargs):
        if layer == Dropout and self.dropout_rate == 0:
            return inputs
        
        arguments = arguments or {}
        
        name = kwargs.get('name')
        if name not in self.layers:
            layer = layer(**kwargs)
            name=layer.name
            self.layers[name] = layer
            
        return self.layers[name](inputs,**arguments)
    
    def set_inputs(self,inputs,additional_input_layers=None):
        if inputs is None:
            inputs = []
        elif not isinstance(inputs,list):
            inputs = [inputs]
        
        inputs = inputs[:]
        
        if additional_input_layers is not None:
            if not isinstance(additional_input_layers,list):
                additional_input_layers = [additional_input_layers]
            inputs.extend(additional_input_layers)
        self.inputs = inputs
        if len(inputs) > 1:
            self.input = inputs
        else:
            self.input = inputs[0]
    
    def set_outputs(self,outputs):
        if not isinstance(outputs,list):
            outputs = [outputs]
        outputs = outputs[:]
        self.outputs = outputs
        if len(outputs) > 1:
            self.output = outputs
        else:
            self.output = outputs[0]
            
    
    def apply_embeddings(self,inputs):
        raise NotImplementedError
        
    def apply_main_layers(self,inputs,index):
        raise NotImplementedError
    
    def apply_final_layers(self,inputs):
        raise NotImplementedError
        
    def compute_attention_mask(self,inputs=None):
        return self.attention_mask
    
    def compute_position_bias(self,inputs=None):
        return self.position_bias
    
    @property
    def initializer(self):
        return keras.initializers.TruncatedNormal(stddev=0.02)
    
    def simplify(self,inputs):
        inputs = [i for i in inputs if i is not None]
        if len(inputs) == 1:
            inputs = inputs[0]
        return inputs
    
    def load_variable(self,checkpoint,name):
        return tf.train.load_variable(checkpoint,name)
    
    def create_variable(self,name,value):
        return tf.Variable(value,name=name)
    
    def variable_mapping(self):
        return {}
    
    def load_weights_from_checkpoint(self, checkpoint, mapping=None):
        """根据mapping从checkpoint加载权重
        """
        mapping = mapping or self.variable_mapping()
        mapping = {k: v for k, v in mapping.items() if k in self.layers}

        weight_value_pairs = []
        for layer, variables in mapping.items():
            layer = self.layers[layer]
            weights = layer.trainable_weights
            values = [self.load_variable(checkpoint, v) for v in variables]

            if isinstance(layer, MultiHeadAttention):
                """如果key_size不等于head_size，则可以通过
                正交矩阵将相应的权重投影到合适的shape。
                """
                count = 2
                if layer.use_bias:
                    count += 2
                heads = self.num_attention_heads
                head_size = self.attention_head_size
                key_size = self.attention_key_size
                W = np.linalg.qr(np.random.randn(key_size, head_size))[0].T
                if layer.attention_scale:
                    W = W * key_size**0.25 / head_size**0.25
                for i in range(count):
                    w, v = weights[i], values[i]
                    w_shape, v_shape = K.int_shape(w), v.shape
                    if w_shape[-1] != v_shape[-1]:
                        pre_shape = w_shape[:-1]
                        v = v.reshape(pre_shape + (heads, head_size))
                        v = np.dot(v, W)
                        v = v.reshape(pre_shape + (heads * key_size,))
                        values[i] = v

            weight_value_pairs.extend(zip(weights, values))

        K.batch_set_value(weight_value_pairs)

    def save_weights_as_checkpoint(self, filename, mapping=None):
        """根据mapping将权重保存为checkpoint格式
        """
        mapping = mapping or self.variable_mapping()
        mapping = {k: v for k, v in mapping.items() if k in self.layers}

        with tf.Graph().as_default():
            for layer, variables in mapping.items():
                layer = self.layers[layer]
                values = K.batch_get_value(layer.trainable_weights)
                for name, value in zip(variables, values):
                    self.create_variable(name, value)
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                saver = tf.train.Saver()
                saver.save(sess, filename, write_meta_graph=False)



class BERT(Transformer):
    def __init__(self,
                 max_position,
                 with_pool=False,
                 with_nsp=False,
                 with_mlm=False,
                 custom_position_ids=False,
                 **kwargs):
        super(BERT,self).__init__(**kwargs)
        self.max_position = max_position
        self.with_pool = with_pool
        self.with_nsp = with_nsp
        self.with_mlm = with_mlm
        self.custom_position_ids = custom_position_ids
    
    def get_inputs(self):
        x_in = Input(shape=(self.sequence_length,),name='Input-Token')
        s_in = Input(shape=(self.sequence_length,),name='Input-Segment')
        if self.custom_position_ids:
            p_in = Input(shape=(self.sequence_length,),name='Input-Position')
            return [x_in,s_in,p_in]
        return [x_in,s_in]
    
    def apply_embeddings(self,inputs):
        x,s = inputs[:2]
        z = self.layer_norm_conds[0]
        if self.custom_position_ids:
            p = input[2]
        else:
            p = None
            
        x = self.apply(
                        inputs=x,
                        layer=Embedding,
                        input_dim=self.vocab_size,
                        output_dim=self.embedding_size,
                        embeddings_initializer=self.initializer,
                        mask_zero=True,
                        name='Embedding-Token'
                       )

        s = self.apply(
                        inputs=s,
                        layer=Embedding,
                        input_dim=2,
                        output_dim=self.embedding_size,
                        embeddings_initializer=self.initializer,
                        name='Embedding-Segment'
                      )
        
        x = self.apply(
                        inputs=[x,s],
                        layer=Add,
                        name='Embedding-Token-Segment'
                        )
        
        x = self.apply(
                        inputs=self.simplify([x,p]),
                        layer=PositionEmbedding,
                        input_dim=self.max_position,
                        output_dim=self.embedding_size,
                        merge_mode='add',
                        embeddings_initializer=self.initializer,
                        custom_position_ids=self.custom_position_ids,
                        name='Embedding-Position'
                     )
        
        x = self.apply(
                        inputs=self.simplify([x,z]),
                        layer=LayerNormalization,
                        conditional=(z is not None),
                        hidden_units=self.layer_norm_conds[1],
                        hidden_activation=self.layer_norm_conds[2],
                        hidden_initializer=self.initializer,
                        name='Embedding-Norm'
                     )
        
        x = self.apply(
                        inputs=x,
                        layer=Dropout,
                        rate=self.dropout_rate,
                        name='Embedding-Dropout'
                      )
        
        if self.embedding_size != self.hidden_size:
            x = self.apply(
                            inputs=x,
                            layer=Dense,
                            units=self.hidden_size,
                            kernel_initializer=self.initializer,
                            name='Embedding-Mapping'
                          )

        return x

    def apply_main_layers(self, inputs, index):
        """BERT的主体是基于Self-Attention的模块
        顺序：Att --> Add --> LN --> FFN --> Add --> LN
        """
        x = inputs
        z = self.layer_norm_conds[0]

        attention_name = 'Transformer-%d-MultiHeadSelfAttention' % index
        feed_forward_name = 'Transformer-%d-FeedForward' % index
        attention_mask = self.compute_attention_mask(index)

        # Self Attention
        xi, x, arguments = x, [x, x, x], {'a_mask': None}
        if attention_mask is not None:
            arguments['a_mask'] = True
            x.append(attention_mask)

        x = self.apply(
            inputs=x,
            layer=MultiHeadAttention,
            arguments=arguments,
            heads=self.num_attention_heads,
            head_size=self.attention_head_size,
            key_size=self.attention_key_size,
            kernel_initializer=self.initializer,
            name=attention_name
        )
        x = self.apply(
            inputs=x,
            layer=Dropout,
            rate=self.dropout_rate,
            name='%s-Dropout' % attention_name
        )
        x = self.apply(
            inputs=[xi, x], layer=Add, name='%s-Add' % attention_name
        )
        x = self.apply(
            inputs=self.simplify([x, z]),
            layer=LayerNormalization,
            conditional=(z is not None),
            hidden_units=self.layer_norm_conds[1],
            hidden_activation=self.layer_norm_conds[2],
            hidden_initializer=self.initializer,
            name='%s-Norm' % attention_name
        )

        # Feed Forward
        xi = x
        x = self.apply(
            inputs=x,
            layer=FeedForward,
            units=self.intermediate_size,
            activation=self.hidden_act,
            kernel_initializer=self.initializer,
            name=feed_forward_name
        )
        x = self.apply(
            inputs=x,
            layer=Dropout,
            rate=self.dropout_rate,
            name='%s-Dropout' % feed_forward_name
        )
        x = self.apply(
            inputs=[xi, x], layer=Add, name='%s-Add' % feed_forward_name
        )
        x = self.apply(
            inputs=self.simplify([x, z]),
            layer=LayerNormalization,
            conditional=(z is not None),
            hidden_units=self.layer_norm_conds[1],
            hidden_activation=self.layer_norm_conds[2],
            hidden_initializer=self.initializer,
            name='%s-Norm' % feed_forward_name
        )

        return x

    def apply_final_layers(self, inputs):
        """根据剩余参数决定输出
        """
        x = inputs
        z = self.layer_norm_conds[0]
        outputs = [x]

        if self.with_pool or self.with_nsp:
            # Pooler部分（提取CLS向量）
            x = outputs[0]
            x = self.apply(
                inputs=x,
                layer=Lambda,
                function=lambda x: x[:, 0],
                name='Pooler'
            )
            pool_activation = 'tanh' if self.with_pool is True else self.with_pool
            x = self.apply(
                inputs=x,
                layer=Dense,
                units=self.hidden_size,
                activation=pool_activation,
                kernel_initializer=self.initializer,
                name='Pooler-Dense'
            )
            if self.with_nsp:
                # Next Sentence Prediction部分
                x = self.apply(
                    inputs=x,
                    layer=Dense,
                    units=2,
                    activation='softmax',
                    kernel_initializer=self.initializer,
                    name='NSP-Proba'
                )
            outputs.append(x)

        if self.with_mlm:
            # Masked Language Model部分
            x = outputs[0]
            x = self.apply(
                inputs=x,
                layer=Dense,
                units=self.embedding_size,
                activation=self.hidden_act,
                kernel_initializer=self.initializer,
                name='MLM-Dense'
            )
            x = self.apply(
                inputs=self.simplify([x, z]),
                layer=LayerNormalization,
                conditional=(z is not None),
                hidden_units=self.layer_norm_conds[1],
                hidden_activation=self.layer_norm_conds[2],
                hidden_initializer=self.initializer,
                name='MLM-Norm'
            )
            x = self.apply(
                inputs=x,
                layer=Embedding,
                arguments={'mode': 'dense'},
                name='Embedding-Token'
            )
            x = self.apply(inputs=x, layer=BiasAdd, name='MLM-Bias')
            mlm_activation = 'softmax' if self.with_mlm is True else self.with_mlm
            x = self.apply(
                inputs=x,
                layer=Activation,
                activation=mlm_activation,
                name='MLM-Activation'
            )
            outputs.append(x)

        if len(outputs) == 1:
            outputs = outputs[0]
        elif len(outputs) == 2:
            outputs = outputs[1]
        else:
            outputs = outputs[1:]

        return outputs

    def load_variable(self, checkpoint, name):
        """加载单个变量的函数
        """
        variable = super(BERT, self).load_variable(checkpoint, name)
        if name in [
            'bert/embeddings/word_embeddings',
            'cls/predictions/output_bias',
        ]:
            if self.keep_tokens is None:
                return variable
            else:
                return variable[self.keep_tokens]
        elif name == 'cls/seq_relationship/output_weights':
            return variable.T
        else:
            return variable

    def create_variable(self, name, value):
        """在tensorflow中创建一个变量
        """
        if name == 'cls/seq_relationship/output_weights':
            value = value.T
        return super(BERT, self).create_variable(name, value)

    def variable_mapping(self):
        """映射到官方BERT权重格式
        """
        mapping = {
            'Embedding-Token': ['bert/embeddings/word_embeddings'],
            'Embedding-Segment': ['bert/embeddings/token_type_embeddings'],
            'Embedding-Position': ['bert/embeddings/position_embeddings'],
            'Embedding-Norm': [
                'bert/embeddings/LayerNorm/beta',
                'bert/embeddings/LayerNorm/gamma',
            ],
            'Embedding-Mapping': [
                'bert/encoder/embedding_hidden_mapping_in/kernel',
                'bert/encoder/embedding_hidden_mapping_in/bias',
            ],
            'Pooler-Dense': [
                'bert/pooler/dense/kernel',
                'bert/pooler/dense/bias',
            ],
            'NSP-Proba': [
                'cls/seq_relationship/output_weights',
                'cls/seq_relationship/output_bias',
            ],
            'MLM-Dense': [
                'cls/predictions/transform/dense/kernel',
                'cls/predictions/transform/dense/bias',
            ],
            'MLM-Norm': [
                'cls/predictions/transform/LayerNorm/beta',
                'cls/predictions/transform/LayerNorm/gamma',
            ],
            'MLM-Bias': ['cls/predictions/output_bias'],
        }

        for i in range(self.num_hidden_layers):
            prefix = 'bert/encoder/layer_%d/' % i
            mapping.update({
                'Transformer-%d-MultiHeadSelfAttention' % i: [
                    prefix + 'attention/self/query/kernel',
                    prefix + 'attention/self/query/bias',
                    prefix + 'attention/self/key/kernel',
                    prefix + 'attention/self/key/bias',
                    prefix + 'attention/self/value/kernel',
                    prefix + 'attention/self/value/bias',
                    prefix + 'attention/output/dense/kernel',
                    prefix + 'attention/output/dense/bias',
                ],
                'Transformer-%d-MultiHeadSelfAttention-Norm' % i: [
                    prefix + 'attention/output/LayerNorm/beta',
                    prefix + 'attention/output/LayerNorm/gamma',
                ],
                'Transformer-%d-FeedForward' % i: [
                    prefix + 'intermediate/dense/kernel',
                    prefix + 'intermediate/dense/bias',
                    prefix + 'output/dense/kernel',
                    prefix + 'output/dense/bias',
                ],
                'Transformer-%d-FeedForward-Norm' % i: [
                    prefix + 'output/LayerNorm/beta',
                    prefix + 'output/LayerNorm/gamma',
                ],
            })

        return mapping


def extend_with_language_model(BaseModel):
    """添加下三角的Attention Mask（语言模型用）
    """
    class LanguageModel(BaseModel):
        """带下三角Attention Mask的派生模型
        """
        def __init__(self, *args, **kwargs):
            super(LanguageModel, self).__init__(*args, **kwargs)
            self.with_mlm = self.with_mlm or True

        def compute_attention_mask(self, inputs=None):
            """重载此函数即可
            """
            if self.attention_mask is None:

                def lm_mask(s):
                    seq_len = K.shape(s)[1]
                    idxs = K.arange(0, seq_len)
                    mask = idxs[None, :] <= idxs[:, None]
                    mask = K.cast(mask, K.floatx())
                    return mask[None, None]

                self.attention_mask = self.apply(
                    inputs=self.inputs[1],
                    layer=Lambda,
                    function=lm_mask,
                    name='Attention-LM-Mask'
                )

            return self.attention_mask

    return LanguageModel




def build_transformer_model(
    config_path=None,
    checkpoint_path=None,
    model='bert',
    application='encoder',
    return_keras_model=True,
    **kwargs
):
    """根据配置文件构建模型，可选加载checkpoint权重
    """
    configs = {}
    if config_path is not None:
        configs.update(json.load(open(config_path)))
    configs.update(kwargs)
    if 'max_position' not in configs:
        configs['max_position'] = configs.get('max_position_embeddings')
    if 'dropout_rate' not in configs:
        configs['dropout_rate'] = configs.get('hidden_dropout_prob')

    model, application = model.lower(), application.lower()

    models = {
        'bert': BERT
    }
    MODEL = models[model]

    if model != 't5':
        if application == 'lm':
            MODEL = extend_with_language_model(MODEL)

    transformer = MODEL(**configs)
    transformer.build(**configs)

    if checkpoint_path is not None:
        transformer.load_weights_from_checkpoint(checkpoint_path)

    if return_keras_model:
        return transformer.model
    else:
        return transformer
