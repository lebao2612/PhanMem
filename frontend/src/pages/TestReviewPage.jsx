import Review from "../components/Review";
import { useState } from "react";

function TestReviewPage() {
  const [isReviewOpen, setIsReviewOpen] = useState(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <button
        onClick={() => setIsReviewOpen(true)}
        className="px-6 py-3 bg-blue-600 text-white rounded-lg"
      >
        Mở Review
      </button>

      {isReviewOpen && <Review onClose={() => setIsReviewOpen(false)} />}
    </div>
  );
}

export default TestReviewPage;
