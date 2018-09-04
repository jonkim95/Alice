package main.java;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;

import java.util.List;

public class AvatarMaker {
    private static final String TAG = "NewAvatarActivity";
    private FaceDet mFaceDet;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_avatar);
        Bundle b = getIntent().getExtras();
        String imageDecodable = b.getString("imagePath");
        Bitmap bitmap = null;
        try {
            if (imageDecodable == null) {
                InputStream stream = getResources().openRawResource(R.raw.face4);
                bitmap = BitmapFactory.decodeStream(stream);
            } else {
                Uri imageUri = Uri.fromFile(new File(imageDecodable));
                bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
            }
        } catch (IOException e) {
        }
        if (mFaceDet == null) mFaceDet = new FaceDet(Constants.getFaceShapeModelPath());
        detectFace(bitmap);
    }

    private void detectFace(Bitmap bitmap) {
        final String targetPath = Constants.getFaceShapeModelPath();
        FileUtils.copyFileFromRawToOthers(getApplicationContext(), R.raw.shape_predictor_68_face_landmarks, targetPath);
        List<VisionDetRet> faces = mFaceDet.detect(bitmap);
        Log.d("DetectFace", faces.toString());
        FaceView overlay = (FaceView) findViewById(R.id.faceView);
        overlay.setContent(bitmap, faces);
    }
}