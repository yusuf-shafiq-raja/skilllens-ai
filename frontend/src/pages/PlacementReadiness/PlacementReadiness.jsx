import { useEffect, useState } from "react";

import {
    getPlacementReadiness
} from "../../services/placementReadinessService";

function PlacementReadiness() {

    const [data, setData] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadPlacementReadiness();

    }, []);

    const loadPlacementReadiness = async () => {

        try {

            const response =
                await getPlacementReadiness();

            setData(response);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    };

    if (loading) {

        return <h2>Loading...</h2>;

    }

    if (!data) {

        return <h2>No Placement Readiness Found</h2>;

    }

    return (

        <div className="container mt-4">

            <h2>Placement Readiness</h2>

            <hr />

            <div className="card p-4">

                <h3>

                    Overall Score

                </h3>

                <h1>

                    {data.overall_score}%

                </h1>

                <hr />

                <h4>

                    Readiness Level

                </h4>

                <p>

                    {data.readiness_level}

                </p>

                <hr />

                <h4>

                    Resume Score

                </h4>

                <p>

                    {data.resume_score}%

                </p>

                <hr />

                <h4>

                    Assessment Score

                </h4>

                <p>

                    {data.assessment_score}%

                </p>

                <hr />

                <h4>

                    Competency Score

                </h4>

                <p>

                    {data.competency_score}%

                </p>

                <hr />

                <h4>

                    Recommendation

                </h4>

                <p>

                    {data.recommendation}

                </p>

            </div>

        </div>

    );

}

export default PlacementReadiness;