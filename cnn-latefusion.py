import input_data
import tensorflow as tf
import time
import numpy as np
import network_settings as ns

nowtime = str(time.time())

# -----------------------

print('start')


def cnn_model_1D(features, labels, mode):
    x_image1 = tf.reshape(features["x1"], [-1, ns.IMAGE_SHAPE1[0], ns.IMAGE_SHAPE1[1]])
    x_image2 = tf.reshape(features["x2"], [-1, ns.IMAGE_SHAPE2[0], ns.IMAGE_SHAPE2[1]])

    conv1_1 = tf.layers.conv1d(inputs=x_image1, filters=ns.C1_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool1_1 = tf.layers.max_pooling1d(inputs=conv1_1, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # second conv layer

    conv2_1 = tf.layers.conv1d(inputs=pool1_1, filters=ns.C2_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool2_1 = tf.layers.max_pooling1d(inputs=conv2_1, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # third conv layer

    conv3_1 = tf.layers.conv1d(inputs=pool2_1, filters=ns.C3_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool3_1 = tf.layers.max_pooling1d(inputs=conv3_1, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # first conv layer
    conv1_2 = tf.layers.conv1d(inputs=x_image2, filters=ns.C1_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool1_2 = tf.layers.max_pooling1d(inputs=conv1_2, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # second conv layer

    conv2_2 = tf.layers.conv1d(inputs=pool1_2, filters=ns.C2_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool2_2 = tf.layers.max_pooling1d(inputs=conv2_2, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # third conv layer

    conv3_2 = tf.layers.conv1d(inputs=pool2_2, filters=ns.C3_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool3_2 = tf.layers.max_pooling1d(inputs=conv3_2, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # densely connected layer

    pool3_flat_1 = tf.reshape(pool3_1, [-1, ns.CONV_OUTPUT_SHAPE1 * ns.C3_LAYER_SIZE])
    dense1_1 = tf.layers.dense(inputs=pool3_flat_1, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout1_1 = tf.layers.dropout(inputs=dense1_1, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # densely connected layer

    dense2_1 = tf.layers.dense(inputs=dropout1_1, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout2_1 = tf.layers.dropout(inputs=dense2_1, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # densely connected layer

    pool3_flat_2 = tf.reshape(pool3_2, [-1, ns.CONV_OUTPUT_SHAPE2 * ns.C3_LAYER_SIZE])
    dense1_2 = tf.layers.dense(inputs=pool3_flat_2, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout1_2 = tf.layers.dropout(inputs=dense1_2, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # densely connected layer

    dense2_2 = tf.layers.dense(inputs=dropout1_2, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout2_2 = tf.layers.dropout(inputs=dense2_2, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # combine
    dropout2 = tf.concat([dropout2_1, dropout2_2], 1)

    logits = tf.layers.dense(inputs=dropout2, units=ns.NUM_CLASSES)
    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        # optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
        optimizer = tf.train.AdamOptimizer(learning_rate=ns.LEARNING_RATE)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def cnn_model_2D(features, labels, mode):
    x_image1 = tf.reshape(features["x1"], [-1, ns.IMAGE_SHAPE1[0], ns.IMAGE_SHAPE1[1], ns.IMAGE_SHAPE1[2]])
    x_image2 = tf.reshape(features["x2"], [-1, ns.IMAGE_SHAPE2[0], ns.IMAGE_SHAPE2[1], ns.IMAGE_SHAPE2[2]])

    conv1_1 = tf.layers.conv2d(inputs=x_image1, filters=ns.C1_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool1_1 = tf.layers.max_pooling2d(inputs=conv1_1, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # second conv layer

    conv2_1 = tf.layers.conv2d(inputs=pool1_1, filters=ns.C2_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool2_1 = tf.layers.max_pooling2d(inputs=conv2_1, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # third conv layer

    conv3_1 = tf.layers.conv2d(inputs=pool2_1, filters=ns.C3_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool3_1 = tf.layers.max_pooling2d(inputs=conv3_1, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # first conv layer
    conv1_2 = tf.layers.conv2d(inputs=x_image2, filters=ns.C1_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool1_2 = tf.layers.max_pooling2d(inputs=conv1_2, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # second conv layer

    conv2_2 = tf.layers.conv2d(inputs=pool1_2, filters=ns.C2_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool2_2 = tf.layers.max_pooling2d(inputs=conv2_2, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # third conv layer

    conv3_2 = tf.layers.conv2d(inputs=pool2_2, filters=ns.C3_LAYER_SIZE, kernel_size=conv_shape, padding='SAME',
                               activation=tf.nn.relu)

    pool3_2 = tf.layers.max_pooling2d(inputs=conv3_2, pool_size=ns.MPOOL_SHAPE, strides=ns.MPOOL_SHAPE, padding='SAME')

    # densely connected layer

    pool3_flat_1 = tf.reshape(pool3_1, [-1, ns.CONV_OUTPUT_SHAPE1 * ns.C3_LAYER_SIZE])
    dense1_1 = tf.layers.dense(inputs=pool3_flat_1, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout1_1 = tf.layers.dropout(inputs=dense1_1, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # densely connected layer

    dense2_1 = tf.layers.dense(inputs=dropout1_1, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout2_1 = tf.layers.dropout(inputs=dense2_1, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # densely connected layer

    pool3_flat_2 = tf.reshape(pool3_2, [-1, ns.CONV_OUTPUT_SHAPE2 * ns.C3_LAYER_SIZE])
    dense1_2 = tf.layers.dense(inputs=pool3_flat_2, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout1_2 = tf.layers.dropout(inputs=dense1_2, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # densely connected layer

    dense2_2 = tf.layers.dense(inputs=dropout1_2, units=ns.FC_LAYER_SIZE, activation=tf.nn.relu)
    dropout2_2 = tf.layers.dropout(inputs=dense2_2, rate=ns.DROPOUT_RATE, training=mode == tf.estimator.ModeKeys.TRAIN)

    # combine
    dropout2 = tf.concat([dropout2_1, dropout2_2], 1)

    logits = tf.layers.dense(inputs=dropout2, units=ns.NUM_CLASSES)
    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        # optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
        optimizer = tf.train.AdamOptimizer(learning_rate=ns.LEARNING_RATE)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def main(argv):
    if len(argv) < 5:
        print("Error, Syntax: {0} [train/test] [dataset] [conv dim] [conv width]".format(argv[0]))
        exit()
    global conv_shape
    conv_shape = int(argv[4])
    dataset = argv[2]
    conv_dim = argv[3]
    test = argv[1]

    ns.load_settings_late(dataset, conv_dim)

    run_name = "latefusion-fc1024-lr{0}-adam-{1}conv-{2}".format(ns.LEARNING_RATE, conv_shape, dataset)  # +"-"+nowtime

    print(run_name)

    # Create the Estimator
    if conv_dim == "1d":
        classifier = tf.estimator.Estimator(model_fn=cnn_model_1D, model_dir="models/" + run_name)
    else:
        classifier = tf.estimator.Estimator(model_fn=cnn_model_2D, model_dir="models/" + run_name)

    if test == "train":
        # train

        # Set up logging for predictions
        # Log the values in the "Softmax" tensor with label "probabilities"
        tensors_to_log = {"probabilities": "softmax_tensor"}
        logging_hook = tf.train.LoggingTensorHook(
            tensors=tensors_to_log, every_n_iter=100)

        # Train the model
        train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x1": train_data1, "x2": train_data2},
            y=train_labels,
            batch_size=ns.BATCH_SIZE,
            num_epochs=None,
            shuffle=True)
        classifier.train(
            input_fn=train_input_fn,
            steps=ns.NUM_ITER,
            hooks=[logging_hook])

        # Evaluate the model and print results
        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x1": eval_data1, "x2": eval_data2},
            y=eval_labels,
            num_epochs=1,
            shuffle=False)
        eval_results = classifier.evaluate(input_fn=eval_input_fn)
        print(run_name)
        print(eval_results)
    else:
        # test
        # Evaluate the model and print results
        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x1": eval_data1, "x2": eval_data2},
            y=eval_labels,
            num_epochs=1,
            shuffle=False)
        # eval_results = classifier.evaluate(input_fn=eval_input_fn)

        labels = eval_labels
        predictions = list(classifier.predict(input_fn=eval_input_fn))
        predicted_classes = [p["classes"] for p in predictions]

        from sklearn.metrics import confusion_matrix, classification_report
        print(run_name)

        print(confusion_matrix(labels, predicted_classes))
        print(classification_report(labels, predicted_classes))


if __name__ == "__main__":
    tf.app.run()
