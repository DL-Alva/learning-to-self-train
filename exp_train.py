import os
from tensorflow.python.platform import flags
from trainer.meta_LST import MetaTrainer

FLAGS = flags.FLAGS
### Basic Options (the same as MTL)
flags.DEFINE_integer('way_num', 5, 'number of classes (e.g. 5-way classification)')
flags.DEFINE_integer('shot_num', 1, 'number of examples per class (K for K-shot learning)')
flags.DEFINE_integer('img_size', 84, 'image size')
flags.DEFINE_integer('device_id', 1, 'GPU device ID to run the job.')
flags.DEFINE_float('gpu_rate', 0.9, 'the parameter for the full_gpu_memory_mode')
flags.DEFINE_string('phase', 'meta', 'pre or meta')
flags.DEFINE_string('exp_log_label', 'weights_saving_dir', 'directory for summaries and checkpoints')
flags.DEFINE_string('logdir_base', './', 'directory for logs')
flags.DEFINE_string('dataset','miniImagenet', 'dataset used in the experiment (miniImagenet or tieredImagenet)')
flags.DEFINE_string('data_path', './', 'directory for dataset')
flags.DEFINE_bool('full_gpu_memory_mode', False, 'in this mode, the code occupies GPU memory in advance')
flags.DEFINE_string('exp_name', 'finetune_mini_RN', 'name for the experiment')

### Basic Options used in our experiments
flags.DEFINE_integer('nb_ul_samples', 10, 'number of unlabeled examples per class (K for K-shot learning)')
flags.DEFINE_integer('unfiles_num', 1, 'number of unlabeled files used in the experiment (There are 10 unlabeled samples per class in each file)')
flags.DEFINE_bool('meta_finetune', True, 'if using MTL weights for finetuning')
flags.DEFINE_string('pretrain_w_path', 'pretrain_weights_dir/', 'directory for loading MTL pretraining weights')
flags.DEFINE_string('finetune_w_path', '', 'directory for loading MTL weights')

### Pretrain Phase Options
flags.DEFINE_integer('pre_lr_dropstep', 5000, 'the step number to drop pre_lr')
flags.DEFINE_integer('pretrain_class_num', 64, 'number of classes used in the pre-train phase')
flags.DEFINE_integer('pretrain_batch_size', 64, 'batch_size for the pre-train phase')
flags.DEFINE_integer('pretrain_iterations', 14000, 'number of pretraining iterations.')
flags.DEFINE_integer('pre_sum_step', 10, 'the step number to summary during pretraining')
flags.DEFINE_integer('pre_save_step', 1000, 'the step number to save the pretrain model')
flags.DEFINE_integer('pre_print_step', 1000, 'the step number to print the pretrain results')
flags.DEFINE_float('pre_lr', 0.001, 'the pretrain learning rate')
flags.DEFINE_float('min_pre_lr', 0.0001, 'the pretrain learning rate min')
flags.DEFINE_float('pretrain_dropout_keep', 0.9, 'the dropout keep parameter in the pre-train phase')
flags.DEFINE_string('pretrain_folders', '', 'directory for pre-train data')
flags.DEFINE_string('pretrain_val_folders', '', 'directory for pre-train val data')
flags.DEFINE_bool('pre_lr_stop', False, 'whether stop decrease the pre_lr when it is low')

### Meta Phase Options
flags.DEFINE_integer('meta_sum_step', 10, 'the step number to summary during meta-training')
flags.DEFINE_integer('meta_save_step', 1000, 'the step number to save the model')
flags.DEFINE_integer('meta_print_step', 100, 'the step number to print the meta-train results')
flags.DEFINE_integer('meta_val_print_step', 1000, 'the step number to print the meta-val results during meta-training')
flags.DEFINE_integer('metatrain_iterations', 15000, 'number of meta-train iterations.')
flags.DEFINE_integer('meta_batch_size', 2, 'number of tasks sampled per meta-update')
flags.DEFINE_integer('re_train_epoch_num', 5, 'number of pre_training inner gradient updates.')
flags.DEFINE_integer('train_base_epoch_num', 20, 'number of inner gradient updates during training.')
flags.DEFINE_integer('test_base_epoch_num', 100, 'number of inner gradient updates during test.')
flags.DEFINE_integer('lr_drop_step', 1000, 'the step number to drop meta_lr')
flags.DEFINE_integer('test_iter', 6000, 'iteration to load model')

flags.DEFINE_float('meta_lr', 0.001, 'the meta learning rate of the generator')
flags.DEFINE_float('swn_lr', 0.001, 'the learning rate for swn')
flags.DEFINE_float('min_meta_lr', 0.0001, 'the min meta learning rate of the generator')
flags.DEFINE_float('base_lr', 0.01, 'step size alpha for inner gradient update.')
flags.DEFINE_string('activation', 'leaky_relu', 'leaky_relu, relu, or None')
flags.DEFINE_string('norm', 'batch_norm', 'batch_norm, layer_norm, or None')

flags.DEFINE_string('exp_string','','none')
flags.DEFINE_string('logdir','','none')
flags.DEFINE_string('pretrain_dir','','none')
flags.DEFINE_string('pretrain_weights_path','','none')
flags.DEFINE_string('finetune_weights_path','','none')
flags.DEFINE_string('test_output_dir','','none')


flags.DEFINE_bool('metatrain', True, 'is this the meta-train phase')
flags.DEFINE_bool('base_augmentation', False, 'whether do data augmentation during base learning')
flags.DEFINE_bool('test_base_augmentation', False, 'whether do data augmentation during base learning for meta test')


# Generate Experiment Key Words String
exp_string = 'dataset(' + FLAGS.dataset + ')'
exp_string += '.cls(' + str(FLAGS.way_num) + ')'
exp_string += '.shot(' + str(FLAGS.shot_num) + ')'
exp_string += '.meta_batch(' + str(FLAGS.meta_batch_size) + ')'
exp_string += '.base_epoch(' + str(FLAGS.train_base_epoch_num) + ')'
exp_string += '.meta_lr(' + str(FLAGS.meta_lr) + ')'
exp_string += '.base_lr(' + str(FLAGS.base_lr) + ')'
exp_string += '.pre_iterations(' + str(FLAGS.pretrain_iterations) + ')'
exp_string += '.pre_dropout(' + str(FLAGS.pretrain_dropout_keep) + ')'
exp_string += '.acti(' + str(FLAGS.activation) + ')'
exp_string += '.lr_drop_step(' + str(FLAGS.lr_drop_step) + ')'

if FLAGS.base_augmentation:
    exp_string += '.base_aug(True)'
else:
    exp_string += '.base_aug(False)'

if FLAGS.norm == 'batch_norm':
    exp_string += '.norm(batch)'
elif FLAGS.norm == 'layer_norm':
    exp_string += '.norm(layer)'
elif FLAGS.norm == 'None':
    exp_string += '.norm(none)'
else:
    print('Norm setting not recognized')

exp_string += '.' + FLAGS.exp_name

FLAGS.exp_string = exp_string
print('Parameters: ' + exp_string)

# Generate Log Folders
FLAGS.finetune_w_path = 'pretrain_weights_dir/' + str(FLAGS.shot_num) +'-shot_MTL_weights'
FLAGS.logdir = FLAGS.logdir_base + FLAGS.exp_log_label
FLAGS.pretrain_weights_path = FLAGS.logdir_base + FLAGS.pretrain_w_path + FLAGS.dataset + '/pretrain_weights'
FLAGS.finetune_weights_path = FLAGS.logdir_base + FLAGS.finetune_w_path
FLAGS.test_output_dir = FLAGS.logdir_base + 'test_output_dir'

def main():
    os.environ['CUDA_VISIBLE_DEVICES'] = str(FLAGS.device_id)
    trainer = MetaTrainer()

if __name__ == "__main__":
    main()
